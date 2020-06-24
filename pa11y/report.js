const fs = require("fs");

const issues = require("./pa11y.json");
const scenarios = require("./scenarios");

const categories = [...new Set(scenarios.map((s) => s.category))];

const scenariosByCategory = categories.reduce(
  (by, c) => ({
    ...by,
    [c]: scenarios.filter((s) => s.category === c),
  }),
  {}
);

const issuesByScenario = issues.reduce((by, issue) => {
  by[issue.label] = by[issue.label] || [];

  by[issue.label].push(issue);

  return by;
}, {});

/**
 * String concatenation disguised as lit-html, for syntax highlighting purposes.
 */
const html = (strings, ...values) => {
  return strings.reduce((out, str, i) => {
    const val = values[i] ?? "";
    return out + str + val;
  }, "");
};

const Scenario = (scenario) => {
  const { category, label, path, states } = scenario;
  const fullLabel = `${category} – ${label}`;
  const issues = issuesByScenario[fullLabel] || [];

  return html`
    <div style="margin-left: 3rem;">
      <div style="display: grid; grid-template-columns: 1fr 1fr;">
        <div>
          <h3
            id="scenario-${encodeURIComponent(category)}-${encodeURIComponent(
              label
            )}"
          >
            ${label}
          </h3>
          <p>
            Path:
            <a href="http://localhost:8000${path}"><code>${path}</code></a>
          </p>
          <p>
            Lighthouse:
            <a href="/lighthouse/${fullLabel}.html"
              ><code>${fullLabel}.html</code></a
            >
          </p>
          <details>
            <summary>Scenario</summary>
            <pre><code>${JSON.stringify(scenario, null, 2)}</code></pre>
          </details>
          <details>
            <summary>Issues: ${issues.length}</summary>
            <ul>
              ${issues
                .map(
                  (issue) => html`
                    <li>
                      <p>
                        <code>${issue.runner} ${issue.code}</code>:
                        ${issue.message}
                      </p>
                      <p>${issue.selector}</p>
                    </li>
                  `
                )
                .join("")}
            </ul>
          </details>
        </div>
        <a
          href="/screenshots/${fullLabel}.png"
          aria-label="Open screenshot of ${fullLabel}"
        >
          <img
            src="/screenshots/${fullLabel}.png"
            alt="Screenshot of ${fullLabel}"
            width="300"
            loading="lazy"
          />
        </a>
      </div>
      ${states
        ? states
            .map((s) =>
              Scenario({
                category,
                path,
                ...s,
                label: `${label} - ${s.label}`,
              })
            )
            .join("")
        : ""}
    </div>
  `;
};

const Category = (category, i) => {
  return html`
    <section aria-labelledby="category-${encodeURIComponent(category)}">
      <h2 id="category-${encodeURIComponent(category)}">${category}</h2>
      ${scenariosByCategory[category].map(Scenario).join("")}
    </section>
  `;
};

const OverviewRow = (scenarioLabel) => {
  const issues = issuesByScenario[scenarioLabel];
  if (issues.length === 0) {
    return html` <tr>
      <td>No issues!</td>
    </tr>`;
  }

  const { category, label, scenario, screenshot, lighthouseReport } = issues[0];

  return html`
    <tr>
      <td>
        ${category}
      </td>
      <td>
        ${label}
      </td>
      <td>${issues.length}</td>
      <td>
        <a
          href="#scenario-${encodeURIComponent(category)}-${encodeURIComponent(
            label
          )}"
          >details</a
        >, <a href="http://localhost:8000${scenario.path}">path</a>,
        <a href="/screenshots/${screenshot}">screenshot</a>,
        <a href="/lighthouse/${lighthouseReport}">lighthouse</a>
      </td>
    </tr>
  `;
};

const report = html`
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <title>Django admin tests report | Pa11y + Lighthouse</title>
      <style>
        html {
          font-size: 1.25rem;
          font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu,
            Cantarell, Noto Sans, sans-serif, BlinkMacSystemFont, "Segoe UI",
            Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji",
            "Segoe UI Symbol";
        }

        body {
          max-width: 1260px;
          margin: 0 auto;
          padding: 1rem;
        }
      </style>
    </head>
    <body>
      <main>
        <h1>Django admin accessibility tests</h1>
        <p>
          Automated accessibility tests from
          <a href="https://github.com/thibaudcolas/django_admin_tests"
            >github.com/thibaudcolas/django_admin_tests</a
          >.
        </p>
        <p>
          Generated: <time>${new Date().toISOString().replace("T", " ")}</time>
        </p>
        <p>Running with Axe and HTML CodeSniffer via Pa11y, and Lighthouse.</p>
        <h2 id="overview">Overview</h2>
        <table>
          <caption>
            Overview of test results
          </caption>
          <thead>
            <tr>
              <th>Category</th>
              <th>Scenario</th>
              <th>Issues</th>
              <th>Links</th>
            </tr>
          </thead>
          <tbody>
            ${Object.keys(issuesByScenario).map(OverviewRow).join("")}
          </tbody>
        </table>
        ${categories.map(Category).join("")}
      </main>
    </body>
  </html>
`;

fs.writeFileSync(`${__dirname}/report.html`, report);
