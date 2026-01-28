---
name: performance-profiling
description: Runtime performance profiling using Chrome DevTools and React DevTools. JavaScript snippets for measuring renders, detecting memory leaks, and profiling interactions. Use with Claude Chrome extension for automated performance testing.
---

# Performance Profiling Skill

Runtime performance analysis using browser APIs and React DevTools integration.

## When to Use

- Measuring actual component render times (not just static analysis)
- Detecting unnecessary re-renders at runtime
- Profiling specific user interactions
- Memory leak investigation
- Network waterfall analysis
- Before/after performance comparison

## Prerequisites

1. **Claude Chrome Extension** connected
2. **React DevTools Extension** installed (for React-specific profiling)
3. **Dev server running** with the app loaded

## Tool Reference

| Tool | Purpose |
|------|---------|
| `mcp__claude-in-chrome__javascript_tool` | Execute profiling scripts |
| `mcp__claude-in-chrome__computer` | Screenshot performance panels |
| `mcp__claude-in-chrome__read_console_messages` | Read profiling output |
| `mcp__claude-in-chrome__read_network_requests` | Analyze API performance |

---

## React DevTools Integration

### Check if React DevTools is Available

```javascript
// Execute via mcp__claude-in-chrome__javascript_tool
(function() {
  const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!hook) {
    return { available: false, message: 'React DevTools not installed' };
  }

  const renderers = Array.from(hook.renderers?.values() || []);
  return {
    available: true,
    reactVersion: renderers[0]?.version || 'unknown',
    rendererCount: renderers.length,
    hasProfiler: typeof hook.onCommitFiberRoot === 'function'
  };
})();
```

### Get Component Tree Summary

```javascript
// Get high-level component structure
(function() {
  const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!hook?.getFiberRoots) return { error: 'DevTools not available' };

  const roots = hook.getFiberRoots(1);
  if (!roots?.size) return { error: 'No React roots found' };

  const root = roots.values().next().value;
  const components = [];

  function traverse(fiber, depth = 0) {
    if (!fiber || depth > 3) return; // Limit depth

    if (fiber.type?.name || fiber.type?.displayName) {
      components.push({
        name: fiber.type.displayName || fiber.type.name,
        depth,
        hasState: fiber.memoizedState !== null,
        hasEffects: fiber.flags > 0
      });
    }

    if (fiber.child) traverse(fiber.child, depth + 1);
    if (fiber.sibling) traverse(fiber.sibling, depth);
  }

  traverse(root.current);
  return { components: components.slice(0, 50) }; // Limit output
})();
```

### Monitor Re-renders in Real-Time

```javascript
// Inject render counter - run this BEFORE the interaction
(function() {
  if (window.__PERF_RENDER_LOG__) {
    return { status: 'already_running', renders: window.__PERF_RENDER_LOG__ };
  }

  window.__PERF_RENDER_LOG__ = [];
  const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;

  if (!hook) return { error: 'React DevTools not available' };

  const originalOnCommitFiberRoot = hook.onCommitFiberRoot;

  hook.onCommitFiberRoot = function(rendererID, root, priority) {
    const fiber = root.current;
    const timestamp = performance.now();

    function getUpdatedComponents(fiber, updates = []) {
      if (!fiber) return updates;

      // Check if this fiber was updated
      if (fiber.flags > 0 && (fiber.type?.name || fiber.type?.displayName)) {
        updates.push({
          name: fiber.type.displayName || fiber.type.name,
          flags: fiber.flags,
          time: timestamp
        });
      }

      getUpdatedComponents(fiber.child, updates);
      getUpdatedComponents(fiber.sibling, updates);
      return updates;
    }

    const updates = getUpdatedComponents(fiber);
    if (updates.length > 0) {
      window.__PERF_RENDER_LOG__.push({
        timestamp,
        updates,
        priority
      });
    }

    if (originalOnCommitFiberRoot) {
      originalOnCommitFiberRoot.call(this, rendererID, root, priority);
    }
  };

  return { status: 'monitoring_started', message: 'Perform your interaction, then call getRenderLog()' };
})();
```

### Get Render Log

```javascript
// Call this AFTER the interaction to get results
(function() {
  const log = window.__PERF_RENDER_LOG__ || [];

  // Aggregate by component
  const byComponent = {};
  log.forEach(entry => {
    entry.updates.forEach(update => {
      if (!byComponent[update.name]) {
        byComponent[update.name] = { count: 0, times: [] };
      }
      byComponent[update.name].count++;
      byComponent[update.name].times.push(update.time);
    });
  });

  // Sort by render count (most renders first)
  const sorted = Object.entries(byComponent)
    .map(([name, data]) => ({ name, ...data }))
    .sort((a, b) => b.count - a.count);

  return {
    totalCommits: log.length,
    componentRenders: sorted.slice(0, 20), // Top 20
    suspicious: sorted.filter(c => c.count > 5).map(c => c.name)
  };
})();
```

### Stop Render Monitoring

```javascript
// Clean up the monitoring hook
(function() {
  delete window.__PERF_RENDER_LOG__;
  // Note: Can't easily restore original hook, but it won't cause issues
  return { status: 'monitoring_stopped' };
})();
```

---

## Chrome Performance API

### Measure Interaction Performance

```javascript
// Measure a specific interaction (e.g., button click, navigation)
(function() {
  window.__PERF_MEASURE__ = {
    start: performance.now(),
    marks: [],
    measures: []
  };

  // Clear previous marks
  performance.clearMarks();
  performance.clearMeasures();

  // Mark start
  performance.mark('interaction-start');

  return {
    status: 'measuring',
    message: 'Perform the interaction, then call endMeasure()'
  };
})();
```

### End Measurement

```javascript
// Call after interaction completes
(function() {
  performance.mark('interaction-end');
  performance.measure('interaction', 'interaction-start', 'interaction-end');

  const measure = performance.getEntriesByName('interaction')[0];
  const longTasks = performance.getEntriesByType('longtask') || [];

  // Get all performance entries during the interaction
  const allEntries = performance.getEntriesByType('measure')
    .concat(performance.getEntriesByType('resource'))
    .filter(e => e.startTime >= window.__PERF_MEASURE__?.start);

  return {
    duration: measure?.duration || 0,
    longTasks: longTasks.length,
    resources: allEntries.filter(e => e.entryType === 'resource').length,
    breakdown: {
      total: measure?.duration,
      resources: allEntries
        .filter(e => e.entryType === 'resource')
        .slice(0, 10)
        .map(e => ({ name: e.name.split('/').pop(), duration: e.duration }))
    }
  };
})();
```

### Get Long Tasks

```javascript
// Detect JavaScript tasks blocking the main thread
(function() {
  // Check if PerformanceObserver is available
  if (!window.PerformanceObserver) {
    return { error: 'PerformanceObserver not supported' };
  }

  // Get existing long tasks
  const longTasks = performance.getEntriesByType('longtask') || [];

  return {
    count: longTasks.length,
    tasks: longTasks.map(task => ({
      duration: task.duration,
      startTime: task.startTime,
      name: task.name
    })),
    threshold: '50ms (tasks longer than this block UI)'
  };
})();
```

### Start Long Task Observer

```javascript
// Monitor for long tasks during an interaction
(function() {
  if (window.__LONG_TASK_OBSERVER__) {
    return { status: 'already_observing' };
  }

  window.__LONG_TASKS__ = [];

  window.__LONG_TASK_OBSERVER__ = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      window.__LONG_TASKS__.push({
        duration: entry.duration,
        startTime: entry.startTime,
        attribution: entry.attribution?.[0]?.name || 'unknown'
      });
    }
  });

  window.__LONG_TASK_OBSERVER__.observe({ entryTypes: ['longtask'] });

  return { status: 'observing', message: 'Perform interaction, then call getLongTasks()' };
})();
```

### Get Observed Long Tasks

```javascript
(function() {
  const tasks = window.__LONG_TASKS__ || [];

  // Clean up
  if (window.__LONG_TASK_OBSERVER__) {
    window.__LONG_TASK_OBSERVER__.disconnect();
    delete window.__LONG_TASK_OBSERVER__;
  }

  const result = {
    count: tasks.length,
    totalBlocking: tasks.reduce((sum, t) => sum + t.duration, 0),
    tasks: tasks,
    verdict: tasks.length === 0 ? 'good' :
             tasks.length < 3 ? 'acceptable' : 'needs_optimization'
  };

  delete window.__LONG_TASKS__;
  return result;
})();
```

---

## Memory Profiling

### Get Memory Snapshot

```javascript
// Check current memory usage (Chrome only)
(function() {
  if (!performance.memory) {
    return { error: 'Memory API not available (Chrome only, requires --enable-precise-memory-info flag)' };
  }

  const memory = performance.memory;
  const toMB = (bytes) => (bytes / 1024 / 1024).toFixed(2);

  return {
    usedHeapSize: toMB(memory.usedJSHeapSize) + ' MB',
    totalHeapSize: toMB(memory.totalJSHeapSize) + ' MB',
    heapLimit: toMB(memory.jsHeapSizeLimit) + ' MB',
    usagePercent: ((memory.usedJSHeapSize / memory.jsHeapSizeLimit) * 100).toFixed(1) + '%'
  };
})();
```

### Detect Potential Memory Leaks

```javascript
// Check for common leak patterns
(function() {
  const issues = [];

  // Check for detached DOM nodes (approximate)
  const allElements = document.querySelectorAll('*').length;
  if (allElements > 5000) {
    issues.push({
      type: 'large_dom',
      count: allElements,
      message: 'DOM has over 5000 elements - consider virtualization'
    });
  }

  // Check for event listeners on window
  // Note: Can't directly count, but can check common patterns
  if (window.__REACT_DEVTOOLS_GLOBAL_HOOK__) {
    const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
    const roots = hook.getFiberRoots?.(1);
    if (roots?.size > 1) {
      issues.push({
        type: 'multiple_roots',
        count: roots.size,
        message: 'Multiple React roots detected - may indicate mounting issues'
      });
    }
  }

  // Check for global state accumulation
  const globalKeys = Object.keys(window).filter(k =>
    k.startsWith('__') && !['__REACT', '__webpack'].some(p => k.includes(p))
  );
  if (globalKeys.length > 10) {
    issues.push({
      type: 'global_pollution',
      count: globalKeys.length,
      keys: globalKeys.slice(0, 5),
      message: 'Many global variables detected'
    });
  }

  return {
    issues,
    verdict: issues.length === 0 ? 'no_obvious_leaks' : 'potential_issues_found',
    recommendation: issues.length > 0 ?
      'Take heap snapshots before/after interaction to confirm leaks' :
      'Memory usage appears normal'
  };
})();
```

---

## Network Performance

### Analyze API Calls

```javascript
// Get performance data for API calls
(function() {
  const resources = performance.getEntriesByType('resource')
    .filter(r => r.initiatorType === 'fetch' || r.initiatorType === 'xmlhttprequest');

  const apiCalls = resources.map(r => ({
    url: r.name.split('?')[0].split('/').slice(-2).join('/'),
    duration: r.duration.toFixed(2) + 'ms',
    size: r.transferSize ? (r.transferSize / 1024).toFixed(2) + 'KB' : 'N/A',
    timing: {
      dns: r.domainLookupEnd - r.domainLookupStart,
      connect: r.connectEnd - r.connectStart,
      ttfb: r.responseStart - r.requestStart,
      download: r.responseEnd - r.responseStart
    }
  }));

  // Sort by duration (slowest first)
  apiCalls.sort((a, b) => parseFloat(b.duration) - parseFloat(a.duration));

  return {
    total: apiCalls.length,
    slowest: apiCalls.slice(0, 5),
    totalTime: resources.reduce((sum, r) => sum + r.duration, 0).toFixed(2) + 'ms'
  };
})();
```

---

## Profiling Workflows

### Workflow 1: Component Render Analysis

```
1. Start render monitoring:
   → Execute "Monitor Re-renders in Real-Time" script

2. Perform the interaction:
   → Click button, navigate, filter data, etc.

3. Get render results:
   → Execute "Get Render Log" script

4. Analyze output:
   → Components with count > 5 are suspicious
   → Look for parent components causing cascading re-renders

5. Clean up:
   → Execute "Stop Render Monitoring" script
```

### Workflow 2: Interaction Performance

```
1. Start measurement:
   → Execute "Measure Interaction Performance" script

2. Start long task observer:
   → Execute "Start Long Task Observer" script

3. Perform the interaction

4. End measurement:
   → Execute "End Measurement" script
   → Execute "Get Observed Long Tasks" script

5. Analyze:
   → duration > 100ms = needs optimization
   → longTasks > 0 = UI was blocked
```

### Workflow 3: Memory Leak Detection

```
1. Take initial snapshot:
   → Execute "Get Memory Snapshot" script
   → Note the usedHeapSize

2. Perform the suspected action multiple times:
   → Open/close modal 10 times
   → Navigate away and back 5 times

3. Take final snapshot:
   → Execute "Get Memory Snapshot" script

4. Compare:
   → If usedHeapSize keeps growing = likely leak
   → Run "Detect Potential Memory Leaks" for hints
```

---

## Interpreting Results

### Re-render Analysis

| Render Count | Verdict | Action |
|--------------|---------|--------|
| 1-2 | Normal | No action needed |
| 3-5 | Review | Check if necessary |
| 6+ | Problem | Add memoization or fix parent |

### Interaction Timing

| Duration | Verdict | User Perception |
|----------|---------|-----------------|
| < 100ms | Excellent | Instant |
| 100-300ms | Good | Responsive |
| 300-1000ms | Acceptable | Noticeable delay |
| > 1000ms | Poor | Feels slow |

### Long Tasks

| Count | Verdict | Action |
|-------|---------|--------|
| 0 | Excellent | Smooth UI |
| 1-2 | Acceptable | Minor jank possible |
| 3+ | Problem | Split work, use requestIdleCallback |

### Memory Growth

| Pattern | Verdict | Action |
|---------|---------|--------|
| Stable | Normal | No leaks |
| Grows then stabilizes | Normal | GC working |
| Continuous growth | Leak | Investigate with heap snapshots |

---

## Common Performance Issues

### Issue: Excessive Re-renders

**Symptoms:** Component appears multiple times in render log with count > 5

**Common Causes:**
1. Parent re-renders passing new object/array references
2. Missing `useMemo` for computed values
3. Missing `useCallback` for handlers
4. Zustand selector without `useShallow`

**Fix Pattern:**
```typescript
// Before: Creates new array every render
const items = data.filter(x => x.active);

// After: Memoized
const items = useMemo(() => data.filter(x => x.active), [data]);
```

### Issue: Long Tasks

**Symptoms:** `longTasks` count > 0, UI feels janky

**Common Causes:**
1. Large list rendering without virtualization
2. Expensive computations in render
3. Synchronous data processing

**Fix Pattern:**
```typescript
// Before: Blocks main thread
const result = expensiveComputation(data);

// After: Defer to idle time
requestIdleCallback(() => {
  const result = expensiveComputation(data);
  setResult(result);
});
```

### Issue: Memory Growth

**Symptoms:** `usedHeapSize` keeps increasing

**Common Causes:**
1. Event listeners not cleaned up
2. Refs holding stale data
3. Closures capturing old state
4. Timers not cleared

**Fix Pattern:**
```typescript
// Always clean up in useEffect
useEffect(() => {
  const handler = () => { /* ... */ };
  window.addEventListener('resize', handler);

  return () => window.removeEventListener('resize', handler);
}, []);
```

---

## Integration with Performance Auditor Agent

When the `performance-auditor` agent loads this skill, it can:

1. **Run static analysis** first (existing grep patterns)
2. **Then run runtime profiling** via Chrome extension
3. **Compare findings** - static issues that cause runtime problems
4. **Generate actionable report** with before/after measurements

Example agent workflow:
```
[performance-auditor] Loading performance-profiling skill
[performance-auditor] Static analysis: Found 12 potential issues
[performance-auditor] Runtime profiling: Measuring interaction...
[performance-auditor] Found: DataTable re-renders 8 times on filter
[performance-auditor] Correlation: Static issue #3 (missing useMemo) confirmed
[performance-auditor] ✓ Complete (Critical: 2, Warnings: 5, Measured: 3)
```
