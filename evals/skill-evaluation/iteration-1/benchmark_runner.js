const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const OUTPUT_PATH = path.join(ROOT, 'benchmark.json');
const DEFAULT_EVAL_IDS = [1, 2, 3, 4];
const CONFIGURATIONS = ['with_skill', 'without_skill'];

function parseArgs(argv) {
  const out = {
    evals: DEFAULT_EVAL_IDS,
    runsPerConfiguration: 1,
    skillName: 'harness-engineering',
    skillPath: 'C:/Users/14156/.claude/skills/harness-engineering',
    executorModel: 'deepseek-v4-pro',
    analyzerModel: 'deepseek-v4-pro',
  };

  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--evals' && argv[i + 1]) {
      out.evals = argv[i + 1]
        .split(',')
        .map((v) => Number(v.trim()))
        .filter((v) => Number.isInteger(v));
      i += 1;
    } else if (arg === '--runs' && argv[i + 1]) {
      const n = Number(argv[i + 1]);
      if (Number.isInteger(n) && n > 0) out.runsPerConfiguration = n;
      i += 1;
    } else if (arg === '--executor-model' && argv[i + 1]) {
      out.executorModel = argv[i + 1];
      i += 1;
    } else if (arg === '--analyzer-model' && argv[i + 1]) {
      out.analyzerModel = argv[i + 1];
      i += 1;
    } else if (arg === '--skill-name' && argv[i + 1]) {
      out.skillName = argv[i + 1];
      i += 1;
    } else if (arg === '--skill-path' && argv[i + 1]) {
      out.skillPath = argv[i + 1];
      i += 1;
    }
  }

  return out;
}

function readJsonIfExists(filePath) {
  if (!fs.existsSync(filePath)) return null;
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function normalizeExpectation(expectation) {
  return {
    text: expectation.text,
    passed: typeof expectation.passed === 'boolean' ? expectation.passed : null,
    evidence: expectation.evidence || '',
  };
}

function round(value, digits = 3) {
  if (value === null || value === undefined || Number.isNaN(value)) return null;
  const factor = Math.pow(10, digits);
  return Math.round(value * factor) / factor;
}

function stats(values) {
  if (values.length === 0) {
    return { mean: null, stddev: null, min: null, max: null };
  }

  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const variance = values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / values.length;

  return {
    mean: round(mean),
    stddev: round(Math.sqrt(variance)),
    min: round(Math.min(...values)),
    max: round(Math.max(...values)),
  };
}

function buildPlaceholderExpectations(assertions) {
  return assertions.map((text) => ({ text, passed: null, evidence: '' }));
}

function collectRun(evalDir, evalMeta, configuration, runNumber) {
  const runDir = path.join(evalDir, configuration);
  const grading = readJsonIfExists(path.join(runDir, 'grading.json'));
  const timing = readJsonIfExists(path.join(runDir, 'timing.json'));

  if (!grading || !timing) {
    return {
      eval_id: evalMeta.eval_id,
      eval_name: evalMeta.eval_name,
      configuration,
      run_number: runNumber,
      result: {
        pass_rate: null,
        passed: 0,
        failed: 0,
        total: 0,
        time_seconds: null,
        tokens: null,
        tool_calls: null,
        errors: 0,
      },
      expectations: buildPlaceholderExpectations(evalMeta.assertions || []),
      notes: [
        `placeholder: missing grading/timing for ${evalMeta.eval_name}/${configuration}`,
      ],
    };
  }

  const summary = grading.summary || {};
  return {
    eval_id: evalMeta.eval_id,
    eval_name: evalMeta.eval_name,
    configuration,
    run_number: runNumber,
    result: {
      pass_rate: typeof summary.pass_rate === 'number' ? summary.pass_rate : null,
      passed: Number.isInteger(summary.passed) ? summary.passed : 0,
      failed: Number.isInteger(summary.failed) ? summary.failed : 0,
      total: Number.isInteger(summary.total) ? summary.total : 0,
      time_seconds:
        typeof timing.total_duration_seconds === 'number'
          ? timing.total_duration_seconds
          : null,
      tokens: Number.isInteger(timing.total_tokens) ? timing.total_tokens : null,
      tool_calls: null,
      errors: 0,
    },
    expectations: (grading.expectations || []).map(normalizeExpectation),
    notes: [],
  };
}

function summarize(runs, configuration) {
  const filtered = runs.filter(
    (run) => run.configuration === configuration && run.result.pass_rate !== null
  );

  return {
    pass_rate: stats(filtered.map((r) => r.result.pass_rate)),
    time_seconds: stats(
      filtered.map((r) => r.result.time_seconds).filter((v) => v !== null)
    ),
    tokens: stats(filtered.map((r) => r.result.tokens).filter((v) => v !== null)),
  };
}

function formatDelta(withStats, withoutStats) {
  const pick = (obj) => (obj && typeof obj.mean === 'number' ? obj.mean : null);
  const passDiff = pick(withStats.pass_rate) - pick(withoutStats.pass_rate);
  const timeDiff = pick(withStats.time_seconds) - pick(withoutStats.time_seconds);
  const tokenDiff = pick(withStats.tokens) - pick(withoutStats.tokens);

  const signed = (v, digits = 2) => {
    if (v === null || Number.isNaN(v)) return null;
    const x = round(v, digits);
    return `${x >= 0 ? '+' : ''}${x}`;
  };

  return {
    pass_rate: signed(passDiff),
    time_seconds: signed(timeDiff, 1),
    tokens: signed(tokenDiff, 0),
  };
}

function main() {
  const args = parseArgs(process.argv);
  const runs = [];

  for (const evalId of args.evals) {
    const evalDir = path.join(ROOT, `eval-${evalId}-${resolveEvalSlug(evalId)}`);
    const evalMeta = readJsonIfExists(path.join(evalDir, 'eval_metadata.json'));
    if (!evalMeta) continue;

    for (const configuration of CONFIGURATIONS) {
      for (let runNumber = 1; runNumber <= args.runsPerConfiguration; runNumber += 1) {
        runs.push(collectRun(evalDir, evalMeta, configuration, runNumber));
      }
    }
  }

  const withSkill = summarize(runs, 'with_skill');
  const withoutSkill = summarize(runs, 'without_skill');

  const includedEvalIds = Array.from(
    new Set(
      runs
        .filter((r) => r.result.pass_rate !== null)
        .map((r) => r.eval_id)
    )
  ).sort((a, b) => a - b);

  const excludedEvalIds = args.evals.filter((id) => !includedEvalIds.includes(id));

  const benchmark = {
    metadata: {
      skill_name: args.skillName,
      skill_path: args.skillPath,
      executor_model: args.executorModel,
      analyzer_model: args.analyzerModel,
      timestamp: new Date().toISOString(),
      evals_run: args.evals,
      runs_per_configuration: args.runsPerConfiguration,
    },
    runs,
    run_summary: {
      coverage: {
        included_eval_ids: includedEvalIds,
        excluded_eval_ids: excludedEvalIds,
        reason:
          excludedEvalIds.length > 0
            ? 'some evals are placeholders without grading/timing results'
            : 'all requested evals included in summary',
      },
      with_skill: withSkill,
      without_skill: withoutSkill,
      delta: formatDelta(withSkill, withoutSkill),
    },
    notes: [],
  };

  fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(benchmark, null, 2)}\n`, 'utf8');
  console.log(`Wrote ${OUTPUT_PATH}`);
}

function resolveEvalSlug(evalId) {
  const map = {
    1: 'new-project',
    2: 'existing-components',
    3: 'agent-setup',
    4: 'agent-setup-neutral',
    5: 'maintenance-closure',
    6: 'delivery-arc',
    7: 'layer5-product-contract',
    8: 'runtime-facts-over-docs',
  };
  return map[evalId] || `unknown-${evalId}`;
}

main();
