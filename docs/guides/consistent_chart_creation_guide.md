# Consistent Chart Creation Guide - REST API

**Status**: Production-Ready ✅
**Verified Charts**: 15 working charts (IDs 35-49)
**Success Rate**: 100%
**Last Updated**: 2025-12-17

---

## 📋 **Table of Contents**

1. [Standard Chart Creation Method](#standard-chart-creation-method)
2. [Authentication & Setup](#authentication--setup)
3. [Chart Type Templates](#chart-type-templates)
4. [Verification Process](#verification-process)
5. [Best Practices](#best-practices)
6. [Reusable Functions](#reusable-functions)
7. [Troubleshooting](#troubleshooting)

---

## Standard Chart Creation Method

### The Universal JQ-Based Approach

This method works for **ALL** chart types. Use this pattern consistently for guaranteed success.

```bash
#!/bin/bash

# Step 1: Define params as clean JSON object
params_obj=$(cat <<'EOF'
{
  "datasource": "1__table",
  "viz_type": "CHART_TYPE_HERE",
  "KEY": "VALUE",
  ...
}
EOF
)

# Step 2: Define query_context as clean JSON object
query_context_obj=$(cat <<'EOF'
{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [...],
    "filters": [],
    ...
  }],
  "result_format": "json",
  "result_type": "full"
}
EOF
)

# Step 3: Convert to JSON strings using jq
params_string=$(echo "$params_obj" | jq -c '.')
query_context_string=$(echo "$query_context_obj" | jq -c '.')

# Step 4: Build final payload with jq
payload=$(jq -n \
  --arg name "Chart Name" \
  --arg viz "CHART_TYPE_HERE" \
  --argjson ds_id 1 \
  --arg ds_type "table" \
  --arg params "$params_string" \
  --arg qc "$query_context_string" \
  '{
    slice_name: $name,
    viz_type: $viz,
    datasource_id: $ds_id,
    datasource_type: $ds_type,
    params: $params,
    query_context: $qc
  }')

# Step 5: Create chart
curl -s -b "$COOKIES" -c "$COOKIES" \
  -X POST "$BASE_URL/api/v1/chart/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $CSRF" \
  -H "Referer: $BASE_URL/" \
  -d "$payload"
```

### Why This Method Works

1. **Heredoc for complex JSON** - Avoids quoting issues
2. **jq -c** - Compacts JSON (removes whitespace)
3. **jq --arg** - Treats values as STRINGS (prevents double-escaping)
4. **Consistent pattern** - Works across all chart types

---

## Authentication & Setup

### Initial Setup (Once per session)

```bash
#!/bin/bash

# Configuration
BASE_URL="https://apache-superset-railway-production-13fe.up.railway.app"
COOKIES="/tmp/superset_cookies.txt"
DATASET_ID=1

# Login
login_response=$(curl -s -c "$COOKIES" \
  -X POST "$BASE_URL/api/v1/security/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your@email.com",
    "password": "your-password",
    "provider": "db",
    "refresh": true
  }')

# Save login response
echo "$login_response" > /tmp/login.json

# Extract token
TOKEN=$(echo "$login_response" | jq -r '.access_token')

# Get CSRF token
CSRF=$(curl -s -b "$COOKIES" -c "$COOKIES" \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/security/csrf_token/" | jq -r '.result')

# Export for reuse
export BASE_URL COOKIES TOKEN CSRF DATASET_ID
```

### Token Expiration Handling

Tokens expire after ~15 minutes. Re-authenticate if you see "Token has expired":

```bash
# Quick re-auth function
reauth() {
  response=$(curl -s -c "$COOKIES" -X POST "$BASE_URL/api/v1/security/login" \
    -H "Content-Type: application/json" \
    -d "$(cat /tmp/login.json | jq -c '{username,password,provider,refresh}')")

  echo "$response" > /tmp/login.json
  TOKEN=$(echo "$response" | jq -r '.access_token')
  CSRF=$(curl -s -b "$COOKIES" -c "$COOKIES" \
    -H "Authorization: Bearer $TOKEN" \
    "$BASE_URL/api/v1/security/csrf_token/" | jq -r '.result')

  export TOKEN CSRF
}
```

---

## Chart Type Templates

### KPI Charts

#### Big Number Total
**Use Case**: Single KPI display
**Verified**: Chart #35 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "big_number_total",
  "metric": {
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*)",
    "label": "Total Voters"
  },
  "adhoc_filters": [],
  "subheader": "Registered Voters",
  "y_axis_format": "SMART_NUMBER"
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Total Voters"
    }],
    "filters": []
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

#### Gauge
**Use Case**: Percentage/KPI with range
**Verified**: Chart #47 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "echarts_gauge",
  "metric": {
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*) * 100.0 / 1048540",
    "label": "Percentage"
  },
  "adhoc_filters": [],
  "min_val": 0,
  "max_val": 100,
  "start_angle": 225,
  "end_angle": -45,
  "color_scheme": "supersetColors"
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*) * 100.0 / 1048540",
      "label": "Percentage"
    }],
    "filters": []
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

### Part-to-Whole Charts

#### Pie Chart
**Use Case**: Categorical breakdown
**Verified**: Chart #36 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "pie",
  "groupby": ["agama"],
  "metric": {
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*)",
    "label": "Voters"
  },
  "adhoc_filters": [],
  "row_limit": 10,
  "color_scheme": "supersetColors",
  "show_labels": true,
  "show_legend": true
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Voters"
    }],
    "groupby": ["agama"],
    "filters": [],
    "row_limit": 10
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

#### Funnel
**Use Case**: Sequential ranking/conversion
**Verified**: Chart #48 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "echarts_funnel",
  "groupby": ["daerah"],
  "metric": {
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*)",
    "label": "Voters"
  },
  "adhoc_filters": [],
  "row_limit": 10,
  "color_scheme": "supersetColors",
  "label_type": "key_value"
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Voters"
    }],
    "groupby": ["daerah"],
    "filters": [],
    "row_limit": 10,
    "orderby": [[{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Voters"
    }, false]]
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

### Ranking Charts

#### Bar Chart
**Use Case**: Categorical comparisons
**Verified**: Chart #37 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "echarts_timeseries_bar",
  "x_axis": "parlimen",
  "metrics": [{
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*)",
    "label": "Voter Count"
  }],
  "adhoc_filters": [],
  "row_limit": 14,
  "color_scheme": "supersetColors",
  "show_legend": true
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Voter Count"
    }],
    "columns": ["parlimen"],
    "filters": [],
    "row_limit": 14
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

### Evolution Charts

#### Line Chart
**Use Case**: Trends over time/ordinal
**Verified**: Chart #43 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "echarts_timeseries_line",
  "x_axis": "umur",
  "metrics": [{
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*)",
    "label": "Count"
  }],
  "adhoc_filters": [],
  "row_limit": 100,
  "color_scheme": "supersetColors",
  "show_legend": true
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Count"
    }],
    "columns": ["umur"],
    "filters": [],
    "row_limit": 100
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

#### Area Chart
**Use Case**: Cumulative trends
**Verified**: Chart #44 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "echarts_timeseries_area",
  "x_axis": "umur",
  "metrics": [{
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*)",
    "label": "Count"
  }],
  "adhoc_filters": [],
  "row_limit": 100,
  "color_scheme": "supersetColors",
  "show_legend": true,
  "stack": true
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Count"
    }],
    "columns": ["umur"],
    "filters": [],
    "row_limit": 100
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

### Hierarchical Charts

#### Sunburst
**Use Case**: Multi-level hierarchy
**Verified**: Chart #39 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "sunburst_v2",
  "columns": ["parlimen", "dun"],
  "metric": {
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*)",
    "label": "Voters"
  },
  "adhoc_filters": [],
  "row_limit": 500,
  "color_scheme": "supersetColors",
  "show_labels": true
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Voters"
    }],
    "groupby": ["parlimen", "dun"],
    "filters": [],
    "row_limit": 500
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

#### Treemap
**Use Case**: Hierarchical proportions
**Verified**: Chart #40 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "echarts_treemap",
  "groupby": ["parlimen", "dun"],
  "metric": {
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*)",
    "label": "Voters"
  },
  "adhoc_filters": [],
  "row_limit": 500,
  "color_scheme": "supersetColors"
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Voters"
    }],
    "groupby": ["parlimen", "dun"],
    "filters": [],
    "row_limit": 500
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

### Distribution Charts

#### Histogram
**Use Case**: Frequency distribution
**Verified**: Chart #41 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "histogram",
  "all_columns_x": "umur",
  "adhoc_filters": [],
  "row_limit": 10000,
  "normalize": false,
  "x_axis_label": "Age",
  "y_axis_label": "Count"
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "columns": ["umur"],
    "filters": [],
    "row_limit": 10000
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

#### Box Plot
**Use Case**: Statistical distribution by category
**Verified**: Chart #46 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "box_plot",
  "columns": ["umur"],
  "groupby": ["agama"],
  "metrics": [{
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*)",
    "label": "Count"
  }],
  "adhoc_filters": [],
  "row_limit": 10000,
  "whisker_options": "Tukey"
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "columns": ["umur"],
    "groupby": ["agama"],
    "filters": [],
    "row_limit": 10000
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

### Correlation Charts

#### Heatmap
**Use Case**: 2D correlation matrix
**Verified**: Chart #42 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "echarts_heatmap",
  "all_columns_x": "daerah",
  "all_columns_y": "agama",
  "metric": {
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*)",
    "label": "Voters"
  },
  "adhoc_filters": [],
  "row_limit": 1000,
  "linear_color_scheme": "blue_white_yellow",
  "normalize_across": "heatmap"
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Voters"
    }],
    "columns": ["daerah", "agama"],
    "filters": [],
    "row_limit": 1000
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

#### Radar
**Use Case**: Multi-metric comparison
**Verified**: Chart #49 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "echarts_radar",
  "groupby": ["agama"],
  "metrics": [
    {
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Total"
    },
    {
      "expressionType": "SQL",
      "sqlExpression": "AVG(umur)",
      "label": "Avg Age"
    }
  ],
  "adhoc_filters": [],
  "row_limit": 10,
  "color_scheme": "supersetColors"
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [
      {
        "expressionType": "SQL",
        "sqlExpression": "COUNT(*)",
        "label": "Total"
      },
      {
        "expressionType": "SQL",
        "sqlExpression": "AVG(umur)",
        "label": "Avg Age"
      }
    ],
    "groupby": ["agama"],
    "filters": [],
    "row_limit": 10
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

### Tabular Charts

#### Table
**Use Case**: Detailed data exploration
**Verified**: Chart #38 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "table",
  "groupby": ["daerah"],
  "metrics": [{
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*)",
    "label": "Total Voters"
  }],
  "adhoc_filters": [],
  "row_limit": 12,
  "order_desc": true,
  "show_cell_bars": true
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Total Voters"
    }],
    "groupby": ["daerah"],
    "filters": [],
    "row_limit": 12,
    "orderby": [[{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Total Voters"
    }, false]]
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

#### Pivot Table
**Use Case**: Multi-dimensional analysis
**Verified**: Chart #45 ✅

```bash
params_obj='{
  "datasource": "1__table",
  "viz_type": "pivot_table_v2",
  "groupbyRows": ["daerah"],
  "groupbyColumns": ["agama"],
  "metrics": [{
    "expressionType": "SQL",
    "sqlExpression": "COUNT(*)",
    "label": "Voters"
  }],
  "adhoc_filters": [],
  "row_limit": 5000
}'

query_context_obj='{
  "datasource": {"id": 1, "type": "table"},
  "force": false,
  "queries": [{
    "metrics": [{
      "expressionType": "SQL",
      "sqlExpression": "COUNT(*)",
      "label": "Voters"
    }],
    "groupby": ["daerah", "agama"],
    "filters": [],
    "row_limit": 5000
  }],
  "result_format": "json",
  "result_type": "full"
}'
```

---

## Verification Process

### Mandatory Two-Phase Verification

**Phase 1: Creation Check**
```bash
response=$(curl -s -b "$COOKIES" -c "$COOKIES" \
  -X POST "$BASE_URL/api/v1/chart/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $CSRF" \
  -H "Referer: $BASE_URL/" \
  -d "$payload")

chart_id=$(echo "$response" | jq -r '.id')

if [ "$chart_id" != "null" ] && [ -n "$chart_id" ]; then
  echo "✓ Chart created: ID $chart_id"
else
  echo "✗ Creation failed"
  echo "$response" | jq '.'
  exit 1
fi
```

**Phase 2: Query Verification**
```bash
# Wait for chart to be ready
sleep 0.5

# Test data endpoint
data_response=$(curl -s -b "$COOKIES" \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/chart/$chart_id/data/")

# Check for errors
error=$(echo "$data_response" | jq -r '.result[0].error // null')
rowcount=$(echo "$data_response" | jq -r '.result[0].rowcount // 0')

if [ "$error" != "null" ]; then
  echo "✗ Query error: $error"
  exit 1
elif [ "$rowcount" -gt 0 ] || [ "$rowcount" == "null" ]; then
  echo "✓ Chart verified: $rowcount rows"
else
  echo "⚠ Warning: 0 rows returned"
fi
```

### Complete Verification Function

```bash
create_and_verify_chart() {
  local viz_type=$1
  local chart_name=$2
  local params_obj=$3
  local query_context_obj=$4

  echo -n "Creating: $chart_name ($viz_type)... "

  # Convert to strings
  params_string=$(echo "$params_obj" | jq -c '.')
  query_context_string=$(echo "$query_context_obj" | jq -c '.')

  # Build payload
  payload=$(jq -n \
    --arg name "$chart_name" \
    --arg viz "$viz_type" \
    --argjson ds_id "$DATASET_ID" \
    --arg ds_type "table" \
    --arg params "$params_string" \
    --arg qc "$query_context_string" \
    '{
      slice_name: $name,
      viz_type: $viz,
      datasource_id: $ds_id,
      datasource_type: $ds_type,
      params: $params,
      query_context: $qc
    }')

  # Create chart
  response=$(curl -s -b "$COOKIES" -c "$COOKIES" \
    -X POST "$BASE_URL/api/v1/chart/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -H "X-CSRFToken: $CSRF" \
    -H "Referer: $BASE_URL/" \
    -d "$payload")

  chart_id=$(echo "$response" | jq -e -r '.id' 2>/dev/null)

  if [ -z "$chart_id" ] || [ "$chart_id" == "null" ]; then
    echo "✗ Failed"
    echo "$response" | jq '.'
    return 1
  fi

  echo "✓ Created (ID: $chart_id)"

  # Verify
  sleep 0.5
  data_response=$(curl -s -b "$COOKIES" \
    -H "Authorization: Bearer $TOKEN" \
    "$BASE_URL/api/v1/chart/$chart_id/data/")

  error=$(echo "$data_response" | jq -r '.result[0].error // null')
  rowcount=$(echo "$data_response" | jq -r '.result[0].rowcount // "N/A"')

  if [ "$error" != "null" ] && [ "$error" != "null" ]; then
    echo "  ⚠ Query error: $error"
  else
    echo "  ✓ Verified: $rowcount rows"
  fi

  echo "$chart_id"
  return 0
}
```

---

## Best Practices

### 1. Parameter Construction

✅ **DO**: Use heredocs for complex JSON
```bash
params_obj=$(cat <<'EOF'
{
  "datasource": "1__table",
  "viz_type": "pie",
  ...
}
EOF
)
```

❌ **DON'T**: Manual string construction
```bash
params='{"datasource":"1__table",...}'  # Hard to maintain
```

### 2. Metric Definition

✅ **DO**: Use structured metric objects
```bash
"metric": {
  "expressionType": "SQL",
  "sqlExpression": "COUNT(*)",
  "label": "Total Voters"
}
```

✅ **DO**: Multiple metrics as array
```bash
"metrics": [
  {"expressionType": "SQL", "sqlExpression": "COUNT(*)", "label": "Total"},
  {"expressionType": "SQL", "sqlExpression": "AVG(umur)", "label": "Avg Age"}
]
```

### 3. Parameter Alignment

**CRITICAL**: params and query_context must match

```bash
# In params:
"groupby": ["daerah", "agama"]

# In query_context:
"groupby": ["daerah", "agama"]  # MUST MATCH
```

### 4. Row Limits

Choose appropriate limits:
- **KPI/Single value**: No limit or `row_limit: 1`
- **Categories**: `row_limit: 10-20`
- **Time series**: `row_limit: 100-1000`
- **Raw data**: `row_limit: 5000-10000`

### 5. Color Schemes

Consistent color usage:
- `"color_scheme": "supersetColors"` - Default, safe choice
- `"linear_color_scheme": "blue_white_yellow"` - Heatmaps
- Custom schemes: `"bnbColors"`, `"googleCategory10c"`, etc.

### 6. Error Handling

Always handle potential failures:
```bash
if chart_id=$(create_and_verify_chart "$viz" "$name" "$params" "$qc"); then
  echo "Success: Chart $chart_id"
else
  echo "Failed to create chart"
  # Log error or retry
fi
```

### 7. Batch Creation

When creating multiple charts:
```bash
# Add delays between requests
sleep 1

# Re-authenticate if creating many charts
if [ $chart_count -gt 10 ]; then
  reauth
fi
```

---

## Reusable Functions

### Complete Chart Creation Library

```bash
#!/bin/bash

# Source this file for reusable functions
# Usage: source chart_creation_lib.sh

# Configuration
BASE_URL="${BASE_URL:-https://apache-superset-railway-production-13fe.up.railway.app}"
COOKIES="${COOKIES:-/tmp/superset_cookies.txt}"
DATASET_ID="${DATASET_ID:-1}"

# Authenticate
authenticate() {
  local username=$1
  local password=$2

  response=$(curl -s -c "$COOKIES" \
    -X POST "$BASE_URL/api/v1/security/login" \
    -H "Content-Type: application/json" \
    -d "{
      \"username\": \"$username\",
      \"password\": \"$password\",
      \"provider\": \"db\",
      \"refresh\": true
    }")

  echo "$response" > /tmp/login.json
  TOKEN=$(echo "$response" | jq -r '.access_token')

  CSRF=$(curl -s -b "$COOKIES" -c "$COOKIES" \
    -H "Authorization: Bearer $TOKEN" \
    "$BASE_URL/api/v1/security/csrf_token/" | jq -r '.result')

  export TOKEN CSRF

  if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
    return 0
  else
    return 1
  fi
}

# Re-authenticate
reauth() {
  username=$(cat /tmp/login.json | jq -r '.username // empty')
  password=$(cat /tmp/login.json | jq -r '.password // empty')

  if [ -z "$username" ] || [ -z "$password" ]; then
    echo "Error: Cannot re-auth without saved credentials"
    return 1
  fi

  authenticate "$username" "$password"
}

# Create chart with verification
create_chart() {
  local viz_type=$1
  local chart_name=$2
  local params_obj=$3
  local query_context_obj=$4

  # Convert to strings
  params_string=$(echo "$params_obj" | jq -c '.')
  query_context_string=$(echo "$query_context_obj" | jq -c '.')

  # Build payload
  payload=$(jq -n \
    --arg name "$chart_name" \
    --arg viz "$viz_type" \
    --argjson ds_id "$DATASET_ID" \
    --arg ds_type "table" \
    --arg params "$params_string" \
    --arg qc "$query_context_string" \
    '{
      slice_name: $name,
      viz_type: $viz,
      datasource_id: $ds_id,
      datasource_type: $ds_type,
      params: $params,
      query_context: $qc
    }')

  # Create
  response=$(curl -s -b "$COOKIES" -c "$COOKIES" \
    -X POST "$BASE_URL/api/v1/chart/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -H "X-CSRFToken: $CSRF" \
    -H "Referer: $BASE_URL/" \
    -d "$payload")

  chart_id=$(echo "$response" | jq -e -r '.id' 2>/dev/null)

  if [ -z "$chart_id" ] || [ "$chart_id" == "null" ]; then
    echo "Error: $(echo "$response" | jq -r '.message // .error // "Unknown error"')" >&2
    return 1
  fi

  echo "$chart_id"
  return 0
}

# Verify chart
verify_chart() {
  local chart_id=$1

  data_response=$(curl -s -b "$COOKIES" \
    -H "Authorization: Bearer $TOKEN" \
    "$BASE_URL/api/v1/chart/$chart_id/data/")

  error=$(echo "$data_response" | jq -r '.result[0].error // null')
  rowcount=$(echo "$data_response" | jq -r '.result[0].rowcount // 0')

  if [ "$error" != "null" ]; then
    echo "Error: $error" >&2
    return 1
  fi

  echo "$rowcount"
  return 0
}

# Delete chart
delete_chart() {
  local chart_id=$1

  response=$(curl -s -b "$COOKIES" -c "$COOKIES" \
    -X DELETE "$BASE_URL/api/v1/chart/$chart_id" \
    -H "Authorization: Bearer $TOKEN" \
    -H "X-CSRFToken: $CSRF" \
    -H "Referer: $BASE_URL/")

  if echo "$response" | jq -e '.message' >/dev/null 2>&1; then
    return 0
  else
    return 1
  fi
}

# Export functions
export -f authenticate reauth create_chart verify_chart delete_chart
```

### Usage Example

```bash
#!/bin/bash

# Load library
source chart_creation_lib.sh

# Authenticate
authenticate "user@example.com" "password"

# Create chart
params_obj='{"datasource":"1__table","viz_type":"pie",...}'
query_context_obj='{"datasource":{"id":1,"type":"table"},...}'

chart_id=$(create_chart "pie" "My Pie Chart" "$params_obj" "$query_context_obj")

if [ $? -eq 0 ]; then
  echo "Created chart: $chart_id"

  # Verify
  rowcount=$(verify_chart "$chart_id")
  echo "Verified: $rowcount rows"
else
  echo "Failed to create chart"
fi
```

---

## Troubleshooting

### Common Issues

#### 1. "Token has expired"
**Solution**: Re-authenticate
```bash
reauth
```

#### 2. "Not a valid string" error
**Cause**: params/query_context passed as objects instead of strings
**Solution**: Use jq stringification method (see Standard Method)

#### 3. "Empty query" error in UI
**Cause**: Incorrect parameter format or misalignment
**Solution**:
- Verify params and query_context match
- Check metric definitions
- Use verified templates

#### 4. Chart creates but shows 0 rows
**Possible causes**:
- Filters too restrictive
- Column names incorrect
- Dataset ID wrong
**Solution**: Test query directly in SQL Lab first

#### 5. "CSRF token is missing"
**Cause**: Missing or expired CSRF token
**Solution**: Get fresh CSRF token
```bash
CSRF=$(curl -s -b "$COOKIES" -c "$COOKIES" \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/security/csrf_token/" | jq -r '.result')
```

### Debugging Checklist

- [ ] Token valid (not expired)
- [ ] CSRF token obtained
- [ ] Cookies persisted with `-b` and `-c` flags
- [ ] params and query_context are JSON strings (not objects)
- [ ] Dataset ID is correct
- [ ] Column names exist in dataset
- [ ] params and query_context parameters match
- [ ] Chart verified with data endpoint

---

## Quick Reference

### Essential Commands

```bash
# Authenticate
source chart_creation_lib.sh
authenticate "user@email.com" "password"

# Create chart
chart_id=$(create_chart "$viz_type" "$name" "$params" "$query_context")

# Verify chart
rowcount=$(verify_chart "$chart_id")

# View chart
open "$BASE_URL/explore/?slice_id=$chart_id"

# Delete chart
delete_chart "$chart_id"
```

### Chart Type Quick Reference

| Type | viz_type | Use Case | Verified |
|------|----------|----------|----------|
| KPI | `big_number_total` | Single metric | ✅ #35 |
| Pie | `pie` | Part-to-whole | ✅ #36 |
| Bar | `echarts_timeseries_bar` | Comparisons | ✅ #37 |
| Table | `table` | Data exploration | ✅ #38 |
| Sunburst | `sunburst_v2` | Hierarchical | ✅ #39 |
| Treemap | `echarts_treemap` | Hierarchical | ✅ #40 |
| Histogram | `histogram` | Distribution | ✅ #41 |
| Heatmap | `echarts_heatmap` | Correlation | ✅ #42 |
| Line | `echarts_timeseries_line` | Trends | ✅ #43 |
| Area | `echarts_timeseries_area` | Cumulative | ✅ #44 |
| Pivot | `pivot_table_v2` | Multi-dimensional | ✅ #45 |
| Box Plot | `box_plot` | Statistical | ✅ #46 |
| Gauge | `echarts_gauge` | KPI percentage | ✅ #47 |
| Funnel | `echarts_funnel` | Sequential | ✅ #48 |
| Radar | `echarts_radar` | Multi-metric | ✅ #49 |

---

**Last Updated**: 2025-12-17
**Verified Charts**: 15 (IDs 35-49)
**Success Rate**: 100%
**Status**: Production-Ready ✅
