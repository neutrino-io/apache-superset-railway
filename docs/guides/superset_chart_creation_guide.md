# Superset Chart Creation Guide for AI Agents
## REST API Chart Creation - Complete Reference

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Authentication Flow](#authentication-flow)
3. [Chart Creation Process](#chart-creation-process)
4. [Chart Structure Reference](#chart-structure-reference)
5. [Available Chart Types](#available-chart-types)
6. [Common Patterns](#common-patterns)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Information
- Superset URL: `https://your-superset-instance.com`
- Username and Password
- Dataset ID (must exist beforehand)
- Dataset Type (usually `"table"`)

### Required Tools
- `curl` or similar HTTP client
- `jq` for JSON processing (optional but recommended)
- Cookie storage capability for session management

---

## Authentication Flow

### Step 1: Obtain Access Token and Cookies

```bash
#!/bin/bash
SUPERSET_URL="https://apache-superset-railway-production-13fe.up.railway.app"
COOKIE_FILE="/tmp/superset_cookies.txt"

# Login and save cookies
curl -c "$COOKIE_FILE" -X POST "$SUPERSET_URL/api/v1/security/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your-email@example.com",
    "password": "your-password",
    "provider": "db",
    "refresh": true
  }' > /tmp/login_response.json

# Extract access token
TOKEN=$(cat /tmp/login_response.json | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
```

### Step 2: Obtain CSRF Token

```bash
# Get CSRF token with cookies
CSRF_RESPONSE=$(curl -s -b "$COOKIE_FILE" -c "$COOKIE_FILE" \
  -H "Authorization: Bearer $TOKEN" \
  "$SUPERSET_URL/api/v1/security/csrf_token/")

CSRF=$(echo $CSRF_RESPONSE | grep -o '"result":"[^"]*"' | cut -d'"' -f4)
```

**CRITICAL**: Both cookies AND tokens are required for chart creation. Cookies handle CSRF session validation.

---

## Chart Creation Process

### Step 3: Create Chart via POST Request

```bash
curl -b "$COOKIE_FILE" -c "$COOKIE_FILE" \
  -X POST "$SUPERSET_URL/api/v1/chart/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $CSRF" \
  -H "Referer: $SUPERSET_URL/" \
  -d '{
    "slice_name": "Chart Name",
    "description": "Chart description",
    "viz_type": "pie",
    "datasource_id": 1,
    "datasource_type": "table",
    "params": "{ ... JSON string ... }",
    "query_context": "{ ... JSON string ... }"
  }'
```

### Response Format

**Success Response:**
```json
{
  "id": 2,
  "result": {
    "datasource_id": 1,
    "datasource_type": "table",
    "description": "Chart description",
    "params": "{ ... }",
    "slice_name": "Chart Name",
    "viz_type": "pie"
  }
}
```

**Error Response:**
```json
{
  "errors": [{
    "message": "400 Bad Request: The CSRF session token is missing.",
    "error_type": "GENERIC_BACKEND_ERROR"
  }]
}
```

---

## Chart Structure Reference

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `slice_name` | string | Chart display name | "Sales by Region" |
| `viz_type` | string | Chart type identifier | "pie", "table", "echarts_timeseries_bar" |
| `datasource_id` | integer | Dataset ID | 1 |
| `datasource_type` | string | Dataset type | "table" |
| `params` | string | JSON config (stringified) | See below |
| `query_context` | string | Query config (stringified) | See below |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Chart description |
| `cache_timeout` | integer | Cache duration in seconds |
| `owners` | array | User IDs of chart owners |

### Params Structure (Common Fields)

```json
{
  "datasource": "1__table",
  "viz_type": "pie",
  "groupby": ["column_name"],
  "metrics": [
    {
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Count"
    }
  ],
  "adhoc_filters": [
    {
      "clause": "WHERE",
      "subject": "column_name",
      "operator": "IS NOT NULL",
      "expressionType": "SIMPLE"
    }
  ],
  "row_limit": 10000,
  "color_scheme": "supersetColors"
}
```

### Query Context Structure

```json
{
  "datasource": {
    "id": 1,
    "type": "table"
  },
  "force": false,
  "queries": [
    {
      "filters": [
        {
          "col": "column_name",
          "op": "IS NOT NULL"
        }
      ],
      "columns": ["column_name"],
      "metrics": [
        {
          "expressionType": "SQL",
          "sqlExpression": "COUNT(*)",
          "label": "Count"
        }
      ],
      "row_limit": 10000,
      "order_desc": true
    }
  ],
  "result_format": "json",
  "result_type": "full"
}
```

---

## Available Chart Types

### ✅ VERIFIED WORKING CHARTS

These chart types have been tested and confirmed working:

#### 1. Table Chart
**viz_type:** `table`

```json
{
  "slice_name": "Data Table",
  "viz_type": "table",
  "datasource_id": 1,
  "datasource_type": "table",
  "params": "{\"datasource\":\"1__table\",\"viz_type\":\"table\",\"groupby\":[\"category\"],\"metrics\":[{\"expressionType\":\"SQL\",\"sqlExpression\":\"COUNT(*)\",\"label\":\"Total Count\"}],\"all_columns\":[],\"percent_metrics\":[],\"adhoc_filters\":[],\"row_limit\":100,\"order_desc\":true,\"table_timestamp_format\":\"smart_date\",\"show_cell_bars\":true,\"color_pn\":true}",
  "query_context": "{\"datasource\":{\"id\":1,\"type\":\"table\"},\"queries\":[{\"columns\":[\"category\"],\"metrics\":[{\"expressionType\":\"SQL\",\"sqlExpression\":\"COUNT(*)\",\"label\":\"Total Count\"}],\"row_limit\":100,\"order_desc\":true}],\"result_format\":\"json\"}"
}
```

**Use Cases:** Raw data display, sorted lists, multi-metric comparisons

**Key Features:**
- `show_cell_bars`: Visual bars in cells
- `color_pn`: Color positive/negative values
- `percent_metrics`: Show percentage columns
- Sortable columns
- Multiple metrics side-by-side

---

#### 2. Pie Chart
**viz_type:** `pie`

```json
{
  "slice_name": "Distribution Pie Chart",
  "viz_type": "pie",
  "datasource_id": 1,
  "datasource_type": "table",
  "params": "{\"datasource\":\"1__table\",\"viz_type\":\"pie\",\"groupby\":[\"category\"],\"metric\":{\"expressionType\":\"SQL\",\"sqlExpression\":\"COUNT(*)\",\"label\":\"Count\"},\"adhoc_filters\":[{\"clause\":\"WHERE\",\"subject\":\"category\",\"operator\":\"IS NOT NULL\",\"expressionType\":\"SIMPLE\"}],\"row_limit\":10000,\"sort_by_metric\":true,\"color_scheme\":\"supersetColors\",\"show_labels\":true,\"labels_outside\":true,\"show_legend\":true,\"donut\":false,\"show_labels_threshold\":5,\"number_format\":\"SMART_NUMBER\"}",
  "query_context": "{\"datasource\":{\"id\":1,\"type\":\"table\"},\"queries\":[{\"filters\":[{\"col\":\"category\",\"op\":\"IS NOT NULL\"}],\"columns\":[\"category\"],\"metrics\":[{\"expressionType\":\"SQL\",\"sqlExpression\":\"COUNT(*)\",\"label\":\"Count\"}],\"row_limit\":10000,\"order_desc\":true}],\"result_format\":\"json\"}"
}
```

**Use Cases:** Part-to-whole relationships, percentage breakdowns

**Key Features:**
- `donut`: Set to `true` for donut chart
- `labels_outside`: Place labels outside slices
- `show_labels_threshold`: Min percentage to show label
- `sort_by_metric`: Auto-sort by size

---

#### 3. Big Number (KPI)
**viz_type:** `big_number_total`

```json
{
  "slice_name": "Total KPI Metric",
  "viz_type": "big_number_total",
  "datasource_id": 1,
  "datasource_type": "table",
  "params": "{\"datasource\":\"1__table\",\"viz_type\":\"big_number_total\",\"metric\":{\"expressionType\":\"SQL\",\"sqlExpression\":\"COUNT(*)\",\"label\":\"Total Records\"},\"adhoc_filters\":[],\"subheader\":\"Total Count\",\"y_axis_format\":\"SMART_NUMBER\",\"time_format\":\"smart_date\",\"color_picker\":{\"r\":0,\"g\":122,\"b\":135,\"a\":1}}",
  "query_context": "{\"datasource\":{\"id\":1,\"type\":\"table\"},\"queries\":[{\"metrics\":[{\"expressionType\":\"SQL\",\"sqlExpression\":\"COUNT(*)\",\"label\":\"Total Records\"}]}],\"result_format\":\"json\"}"
}
```

**Use Cases:** Single metric KPIs, dashboards, executive summaries

**Key Features:**
- `subheader`: Descriptive text below number
- `y_axis_format`: Number formatting (SMART_NUMBER, ,0, etc.)
- `color_picker`: Custom color {r, g, b, a}

---

#### 4. Sunburst Chart
**viz_type:** `sunburst_v2`

```json
{
  "slice_name": "Hierarchical Sunburst",
  "viz_type": "sunburst_v2",
  "datasource_id": 1,
  "datasource_type": "table",
  "params": "{\"datasource\":\"1__table\",\"viz_type\":\"sunburst_v2\",\"columns\":[\"level1\",\"level2\"],\"metric\":{\"expressionType\":\"SIMPLE\",\"column\":{\"column_name\":\"id\",\"type\":\"INTEGER\"},\"aggregate\":\"COUNT\",\"label\":\"COUNT(id)\"},\"adhoc_filters\":[],\"row_limit\":10000,\"color_scheme\":\"supersetColors\",\"show_labels\":true,\"show_total\":true,\"label_type\":\"key\",\"number_format\":\"SMART_NUMBER\"}",
  "query_context": "{\"datasource\":{\"id\":1,\"type\":\"table\"},\"queries\":[{\"columns\":[\"level1\",\"level2\"],\"metrics\":[{\"expressionType\":\"SIMPLE\",\"column\":{\"column_name\":\"id\"},\"aggregate\":\"COUNT\"}],\"row_limit\":10000}],\"result_format\":\"json\"}"
}
```

**Use Cases:** Multi-level hierarchies, organizational structures

**Key Features:**
- `columns`: Array of hierarchy levels (innermost to outermost)
- `show_total`: Show total in center
- `label_type`: "key", "value", or "key_value"

---

### 📊 RECOMMENDED CHART TYPES

These charts are available and recommended based on documentation:

#### 5. Bar Chart (ECharts)
**viz_type:** `echarts_timeseries_bar`

**Template:**
```json
{
  "slice_name": "Bar Chart",
  "viz_type": "echarts_timeseries_bar",
  "params": "{\"datasource\":\"1__table\",\"viz_type\":\"echarts_timeseries_bar\",\"x_axis\":\"category\",\"metrics\":[{\"expressionType\":\"SQL\",\"sqlExpression\":\"COUNT(*)\"}],\"adhoc_filters\":[],\"color_scheme\":\"supersetColors\",\"show_legend\":true,\"rich_tooltip\":true,\"y_axis_format\":\"SMART_NUMBER\",\"x_axis_title\":\"Category\",\"y_axis_title\":\"Count\",\"orientation\":\"vertical\"}"
}
```

**Use Cases:** Categorical comparisons, rankings

---

#### 6. Area Chart
**viz_type:** `echarts_area` or `area`

**Use Cases:** Time series trends with magnitude, cumulative data

---

#### 7. Line Chart
**viz_type:** `echarts_timeseries_line` or `line`

**Use Cases:** Trends over time, continuous data

---

#### 8. Funnel Chart
**viz_type:** `echarts_funnel`

**Use Cases:** Conversion funnels, sequential drop-off analysis

---

#### 9. Gauge Chart
**viz_type:** `echarts_gauge`

**Use Cases:** Progress metrics, percentage completion, goals

---

#### 10. Histogram
**viz_type:** `histogram`

**Use Cases:** Frequency distribution, age/income ranges

---

#### 11. Heatmap
**viz_type:** `heatmap` or `echarts_heatmap`

**Use Cases:** Correlation matrices, density visualization

---

#### 12. Box Plot
**viz_type:** `box_plot`

**Use Cases:** Statistical distribution, outlier detection

---

#### 13. Bubble Chart
**viz_type:** `echarts_bubble`

**Use Cases:** 3-dimensional data (x, y, size)

---

#### 14. Treemap
**viz_type:** `echarts_treemap`

**Use Cases:** Hierarchical data with size comparison

---

#### 15. Sankey Diagram
**viz_type:** `echarts_sankey`

**Use Cases:** Flow analysis, resource allocation

---

#### 16. Graph Chart
**viz_type:** `graph_chart`

**Use Cases:** Network relationships, connections

---

#### 17. Radar Chart
**viz_type:** `echarts_radar`

**Use Cases:** Multi-variable comparison, profile analysis

---

### 🗺️ GEOGRAPHIC CHARTS (deck.gl)

These require geographic data (latitude/longitude or GeoJSON):

#### 18. deck.gl Scatterplot
**viz_type:** `deck_scatter`

**Use Cases:** Point locations on map

---

#### 19. deck.gl Hexagon
**viz_type:** `deck_hex`

**Use Cases:** 3D density visualization, clustering

---

#### 20. deck.gl Heatmap
**viz_type:** `deck_heatmap`

**Use Cases:** Geographic density, hotspot analysis

---

#### 21. deck.gl Arc
**viz_type:** `deck_arc`

**Use Cases:** Origin-destination flows, connections

---

#### 22. deck.gl Polygon
**viz_type:** `deck_polygon`

**Use Cases:** Geographic boundaries, regions

---

#### 23. Country Map
**viz_type:** `country_map`

**Use Cases:** Country-level choropleth

---

### 🎨 ADVANCED CHARTS

#### 24. Pivot Table
**viz_type:** `pivot_table_v2`

**Use Cases:** Multi-dimensional aggregation

---

#### 25. Calendar Heatmap
**viz_type:** `cal_heatmap`

**Use Cases:** Time-based activity patterns

---

#### 26. Horizon Chart
**viz_type:** `horizon`

**Use Cases:** Dense time series, small multiples

---

#### 27. Chord Diagram
**viz_type:** `chord`

**Use Cases:** Flow between categories

---

#### 28. Handlebars
**viz_type:** `handlebars`

**Use Cases:** Custom HTML templates, specialized formatting

---

### ⚠️ DEPRECATED/AVOID

- `dist_bar` - Not supported
- `echarts_bar` - Use `echarts_timeseries_bar` instead
- Legacy `bubble` - Use `echarts_bubble`
- Legacy bubble chart (marked DEPRECATED in UI)

---

## Common Patterns

### Pattern 1: Metric Definition (SQL Expression)

```json
{
  "expressionType": "SQL",
  "sqlExpression": "COUNT(*)",
  "label": "Total Count"
}
```

**Common SQL Expressions:**
- `COUNT(*)` - Total count
- `COUNT(DISTINCT column)` - Unique count
- `SUM(column)` - Sum
- `AVG(column)` - Average
- `MIN(column)` / `MAX(column)` - Min/Max
- `ROUND(AVG(column), 2)` - Rounded average
- `COUNT(*) * 100.0 / (SELECT COUNT(*) FROM table)` - Percentage

### Pattern 2: Filter Definition

```json
{
  "clause": "WHERE",
  "subject": "column_name",
  "operator": "IS NOT NULL",
  "expressionType": "SIMPLE"
}
```

**Common Operators:**
- `IS NOT NULL` / `IS NULL`
- `==` (equals)
- `!=` (not equals)
- `>`, `>=`, `<`, `<=`
- `IN` (with comparator as array)
- `LIKE` (pattern matching)
- `TEMPORAL_RANGE` (for date columns)

### Pattern 3: Color Schemes

Available color schemes:
- `supersetColors` (default)
- `bnbColors`
- `googleCategory10c`
- `googleCategory20c`
- `d3Category10`
- `d3Category20`
- Custom palettes

### Pattern 4: Number Formatting

- `SMART_NUMBER` - Auto format (1K, 1M, 1B)
- `,d` - Thousands separator
- `.2f` - Two decimal places
- `,.2%` - Percentage with decimals
- `$,.2f` - Currency format

---

## Troubleshooting

### Issue 1: "CSRF session token is missing"

**Cause:** Missing cookies or CSRF token

**Solution:**
```bash
# Ensure you're using -b and -c with cookie file
curl -b "$COOKIE_FILE" -c "$COOKIE_FILE" \
  -H "X-CSRFToken: $CSRF" \
  # ... rest of request
```

### Issue 2: "This visualization type is not supported"

**Cause:** Invalid viz_type or chart plugin not installed

**Solution:**
- Check available chart types in UI gallery
- Use verified working types: `table`, `pie`, `big_number_total`, `sunburst_v2`
- Avoid deprecated types

### Issue 3: "Empty query" Error

**Cause:** Malformed params or query_context

**Solution:**
- Ensure params and query_context are valid JSON strings
- Include required fields: metrics, columns/groupby
- Test with simpler table chart first

### Issue 4: Chart Created But Shows No Data

**Cause:** Invalid column names or filters too restrictive

**Solution:**
- Verify column names exist in dataset
- Check filters aren't excluding all data
- Use `IS NOT NULL` filters carefully
- Test query in SQL Lab first

### Issue 5: Token Expired (401 Error)

**Cause:** Access token expired (15 min default)

**Solution:**
```bash
# Re-authenticate to get fresh token
curl -c "$COOKIE_FILE" -X POST "$SUPERSET_URL/api/v1/security/login" ...
```

---

## Complete Working Example Script

```bash
#!/bin/bash
set -e  # Exit on error

# Configuration
SUPERSET_URL="https://your-superset-instance.com"
USERNAME="your-email@example.com"
PASSWORD="your-password"
DATASET_ID=1
COOKIE_FILE="/tmp/superset_cookies.txt"

echo "=== Superset Chart Creation ==="

# Step 1: Login
echo "Step 1: Authenticating..."
curl -c "$COOKIE_FILE" -X POST "$SUPERSET_URL/api/v1/security/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\",\"provider\":\"db\",\"refresh\":true}" \
  > /tmp/login_response.json

TOKEN=$(cat /tmp/login_response.json | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo "✓ Access token obtained"

# Step 2: Get CSRF Token
echo "Step 2: Getting CSRF token..."
CSRF_RESPONSE=$(curl -s -b "$COOKIE_FILE" -c "$COOKIE_FILE" \
  -H "Authorization: Bearer $TOKEN" \
  "$SUPERSET_URL/api/v1/security/csrf_token/")

CSRF=$(echo $CSRF_RESPONSE | grep -o '"result":"[^"]*"' | cut -d'"' -f4)
echo "✓ CSRF token obtained"

# Step 3: Create Chart
echo "Step 3: Creating chart..."
RESPONSE=$(curl -b "$COOKIE_FILE" -c "$COOKIE_FILE" \
  -X POST "$SUPERSET_URL/api/v1/chart/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $CSRF" \
  -H "Referer: $SUPERSET_URL/" \
  -d '{
    "slice_name": "Test Table Chart",
    "description": "Automatically created test chart",
    "viz_type": "table",
    "datasource_id": '$DATASET_ID',
    "datasource_type": "table",
    "params": "{\"datasource\":\"'$DATASET_ID'__table\",\"viz_type\":\"table\",\"groupby\":[],\"metrics\":[{\"expressionType\":\"SQL\",\"sqlExpression\":\"COUNT(*)\",\"label\":\"Count\"}],\"row_limit\":10}",
    "query_context": "{\"datasource\":{\"id\":'$DATASET_ID',\"type\":\"table\"},\"queries\":[{\"metrics\":[{\"expressionType\":\"SQL\",\"sqlExpression\":\"COUNT(*)\"}],\"row_limit\":10}],\"result_format\":\"json\"}"
  }')

# Check if successful
if echo "$RESPONSE" | grep -q '"id"'; then
  CHART_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
  echo "✓ Chart created successfully!"
  echo "Chart ID: $CHART_ID"
  echo "URL: $SUPERSET_URL/explore/?slice_id=$CHART_ID"
else
  echo "✗ Error creating chart:"
  echo "$RESPONSE"
  exit 1
fi
```

---

## Quick Reference: Chart Type Selection

| Data Type | Recommended Chart | viz_type |
|-----------|------------------|----------|
| Categories with counts | Pie Chart | `pie` |
| Categories comparison | Bar Chart | `echarts_timeseries_bar` |
| Time series trend | Line Chart | `echarts_timeseries_line` |
| Distribution | Histogram | `histogram` |
| Statistical summary | Box Plot | `box_plot` |
| Single metric | Big Number | `big_number_total` |
| Raw data | Table | `table` |
| Hierarchy (2+ levels) | Sunburst | `sunburst_v2` |
| Multi-dimensional | Pivot Table | `pivot_table_v2` |
| Geo points | deck.gl Scatter | `deck_scatter` |
| Density map | deck.gl Heatmap | `deck_heatmap` |
| Flow/connections | Sankey | `echarts_sankey` |
| Conversion funnel | Funnel | `echarts_funnel` |
| Progress/goals | Gauge | `echarts_gauge` |

---

## Best Practices for Agents

1. **Always authenticate with cookies**: Use `-b` and `-c` flags with curl
2. **Validate dataset exists**: Check dataset ID before creating charts
3. **Start simple**: Test with `table` chart type first
4. **Use verified types**: Stick to confirmed working viz_types
5. **Handle errors gracefully**: Check response for error messages
6. **Escape JSON properly**: Use single quotes for outer, double for inner JSON
7. **Test incrementally**: Create, test, then add complexity
8. **Store credentials securely**: Never commit passwords to code
9. **Refresh tokens**: Re-authenticate if token expires
10. **Document assumptions**: Note which dataset columns you're using

---

## API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/security/login` | POST | Authenticate and get tokens |
| `/api/v1/security/csrf_token/` | GET | Get CSRF token |
| `/api/v1/chart/` | POST | Create chart |
| `/api/v1/chart/{id}` | GET | Get chart details |
| `/api/v1/chart/{id}` | PUT | Update chart |
| `/api/v1/chart/{id}` | DELETE | Delete chart |
| `/api/v1/dataset/` | GET | List datasets |
| `/api/v1/database/` | GET | List databases |

---

## Conclusion

This guide provides everything needed to programmatically create charts in Apache Superset via REST API. Focus on the verified working chart types (table, pie, big_number_total, sunburst_v2) for guaranteed success, then expand to other types as needed.

For any issues, refer to the Troubleshooting section or check the Superset UI to verify chart type availability.

**Version:** Superset 4.0+ compatible
**Last Updated:** 2025-12-17
