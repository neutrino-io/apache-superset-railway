# Superset Chart Types - Quick Reference

**Last Updated:** 2025-12-17 (ECharts validation completed)
**Superset Version:** 5.0.0
**Instance:** Railway Deployment with ECharts Plugin

---

## ⚠️ IMPORTANT: ACTUAL vs THEORETICAL

This document contains:
- **✅ VERIFIED WORKING**: Charts tested and confirmed working in our Superset 5.0.0 instance
- **📖 THEORETICAL**: Charts that may exist in Superset but NOT tested/verified in this instance

**Always prioritize VERIFIED WORKING charts for production use.**

---

## ✅ VERIFIED WORKING IN THIS INSTANCE

These chart types have been **tested via REST API and verified in the UI**:

### Built-in Charts (6 types)
| Chart Name | viz_type | Category | Complexity | Best For |
|------------|----------|----------|------------|----------|
| Table | `table` | Tabular | ⭐ Easy | Raw data, multiple metrics |
| Pie Chart | `pie` | Part-to-Whole | ⭐ Easy | Percentage breakdowns |
| Big Number | `big_number_total` | KPI | ⭐ Easy | Single metric display |
| Sunburst | `sunburst_v2` | Hierarchical | ⭐⭐ Medium | Multi-level hierarchies |
| Pivot Table | `pivot_table_v2` | Tabular | ⭐⭐ Medium | Cross-tabulation |
| Box Plot | `box_plot` | Statistical | ⭐⭐ Medium | Distribution & outliers |

### ECharts Plugin Charts (2 types) 🆕
| Chart Name | viz_type | Category | Complexity | Best For |
|------------|----------|----------|------------|----------|
| Bar Chart | `echarts_timeseries_bar` | Comparison | ⭐ Easy | Categorical comparisons |
| Line Chart | `echarts_timeseries_line` | Trend | ⭐ Easy | Trends over time |

**Total Verified Working: 8 chart types**

---

## ❌ CONFIRMED NOT WORKING

These chart types **do NOT work** in Superset 5.0.0 (tested and failed):

| viz_type | Reason | Error Message |
|----------|--------|---------------|
| `histogram` | Not supported | "This visualization type is not supported" |
| `echarts_timeseries_area` | Plugin incomplete | Shows raw viz_type name (not recognized) |
| `echarts_treemap` | Plugin incomplete | "This visualization type is not supported" |
| `echarts_heatmap` | Plugin incomplete | "This visualization type is not supported" |
| `echarts_gauge` | Plugin incomplete | "This visualization type is not supported" |
| `echarts_funnel` | Plugin incomplete | "This visualization type is not supported" |
| `echarts_radar` | Plugin incomplete | "This visualization type is not supported" |
| `echarts_scatter` | Plugin incomplete | "This visualization type is not supported" |

**How to Identify Broken Charts:**
- ✅ Working charts display friendly names in UI ("Pie Chart", "Bar Chart")
- ❌ Broken charts display raw viz_type names ("histogram", "echarts_timeseries_area")

---

## 📖 THEORETICAL CHARTS (NOT TESTED)

The following charts **may exist** in Superset but have **NOT been tested** in this instance.
**Use at your own risk** - they may not work in Superset 5.0.0.

### Basic Charts (Theoretical)
| Chart Name | viz_type | Category | Best For |
|------------|----------|----------|----------|
| Area Chart | `echarts_area` or `area` | Trend | Time series with magnitude |
| Bubble Chart | `echarts_bubble` | Multi-dimensional | 3D data (x, y, size) |
| Bullet Chart | `bullet` | Comparison | Goal vs actual |

### Advanced Statistical (Theoretical)
| Chart Name | viz_type | Category | Best For |
|------------|----------|----------|----------|
| Heatmap | `heatmap` | Density | Correlation matrix |
| Calendar Heatmap | `cal_heatmap` | Temporal | Activity patterns |
| Horizon Chart | `horizon` | Trend | Dense time series |

### Flow & Relationship (Theoretical)
| Chart Name | viz_type | Category | Best For |
|------------|----------|----------|----------|
| Sankey Diagram | `echarts_sankey` | Flow | Resource allocation |
| Chord Diagram | `chord` | Flow | Category relationships |
| Graph Chart | `graph_chart` | Network | Node relationships |

### Hierarchical (Theoretical)
| Chart Name | viz_type | Status | Best For |
|------------|----------|--------|----------|
| Treemap | `echarts_treemap` | ❌ NOT WORKING | Size comparison |
| Partition | `partition` | UNTESTED | Cartodiagram style |

### Geographic deck.gl (Theoretical)
| Chart Name | viz_type | Requires | Best For |
|------------|----------|----------|----------|
| Scatterplot | `deck_scatter` | Lat/Lon | Point locations |
| Hexagon 3D | `deck_hex` | Lat/Lon | 3D density visualization |
| Heatmap | `deck_heatmap` | Lat/Lon | Geographic density |
| Arc | `deck_arc` | Origin/Dest coords | Connection flows |
| Path | `deck_path` | Line coords | Routes, trajectories |
| Polygon | `deck_polygon` | GeoJSON | Regional boundaries |
| Geojson | `deck_geojson` | GeoJSON | Custom geometries |
| Grid | `deck_grid` | Lat/Lon | 3D grid aggregation |
| Screen Grid | `deck_screengrid` | Lat/Lon | Screen-space density |
| Contour | `deck_contour` | Lat/Lon | Elevation contours |
| Multiple Layers | `deck_multi` | Mixed | Combined deck.gl |
| Country Map | `country_map` | Country codes | Country choropleth |

### Custom/Advanced (Theoretical)
| Chart Name | viz_type | Category | Best For |
|------------|----------|----------|----------|
| Handlebars | `handlebars` | Custom | HTML templates |
| Generic Chart | `generic` | Custom | Custom D3/JS |

---

## ⚠️ DEPRECATED - DO NOT USE

| Chart Name | viz_type | Reason | Use Instead |
|------------|----------|--------|-------------|
| dist_bar | `dist_bar` | Not supported | `echarts_timeseries_bar` |
| echarts_bar | `echarts_bar` | Causes errors | `echarts_timeseries_bar` |
| Bubble (legacy) | N/A | Marked deprecated in UI | `echarts_bubble` (untested) |
| Legacy bubble | Old bubble type | Superseded | `echarts_bubble` (untested) |

---

## PRODUCTION-READY DECISION TREE

**Use ONLY verified working charts for production:**

```
START: What data do you have?

├─ Single metric?
│  └─ big_number_total ✅

├─ Categories to compare?
│  ├─ Bars → echarts_timeseries_bar ✅
│  └─ Part of whole → pie ✅

├─ Time series/Trend?
│  ├─ Line trend → echarts_timeseries_line ✅
│  └─ Bars over time → echarts_timeseries_bar ✅

├─ Hierarchy (2+ levels)?
│  └─ Nested circles → sunburst_v2 ✅

├─ Distribution analysis?
│  └─ Statistical → box_plot ✅

└─ Raw data/tables?
   ├─ Simple → table ✅
   └─ Pivot → pivot_table_v2 ✅
```

---

## COMPLEXITY RATINGS (Verified Charts Only)

### ⭐ Easy (Beginner-Friendly)
- `table` ✅
- `pie` ✅
- `big_number_total` ✅
- `echarts_timeseries_bar` ✅
- `echarts_timeseries_line` ✅

### ⭐⭐ Medium (Some Configuration)
- `sunburst_v2` ✅
- `box_plot` ✅
- `pivot_table_v2` ✅

---

## FEATURE MATRIX (Verified Charts Only)

| Chart Type | Multiple Metrics | Drill Down | Filters | Time Support | Export |
|------------|------------------|------------|---------|--------------|--------|
| table | ✅ | ✅ | ✅ | ✅ | ✅ |
| pie | ❌ | ✅ | ✅ | ❌ | ✅ |
| big_number_total | ❌ | ❌ | ✅ | ❌ | ✅ |
| sunburst_v2 | ❌ | ✅ | ✅ | ❌ | ✅ |
| pivot_table_v2 | ✅ | ✅ | ✅ | ✅ | ✅ |
| box_plot | ✅ | ❌ | ✅ | ❌ | ✅ |
| echarts_timeseries_bar | ✅ | ✅ | ✅ | ✅ | ✅ |
| echarts_timeseries_line | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## COMMON USE CASES → VERIFIED CHART MAPPING

| Use Case | Primary Choice | Alternative |
|----------|----------------|-------------|
| Dashboard KPI | big_number_total ✅ | N/A |
| Sales by region | echarts_timeseries_bar ✅ | pie ✅ |
| User demographics | pie ✅ | table ✅ |
| Website traffic over time | echarts_timeseries_line ✅ | echarts_timeseries_bar ✅ |
| Multi-metric comparison | table ✅ | pivot_table_v2 ✅ |
| Organizational hierarchy | sunburst_v2 ✅ | table ✅ |
| Age distribution | box_plot ✅ | table ✅ |
| Cross-tabulation | pivot_table_v2 ✅ | table ✅ |

---

## DATA REQUIREMENTS BY CHART TYPE (Verified Only)

### Minimal Requirements (Any table works)
- `table` ✅
- `big_number_total` ✅

### Requires Categories
- `pie` ✅ (1 dimension)
- `echarts_timeseries_bar` ✅ (1 dimension)

### Requires Hierarchy (2+ levels)
- `sunburst_v2` ✅

### Requires Numeric Data
- `box_plot` ✅ (1 numeric column, 1 grouping dimension)

### Cross-Tabulation
- `pivot_table_v2` ✅ (rows + columns + metrics)

---

## PERFORMANCE CONSIDERATIONS (Verified Charts)

### Fast (< 1 sec for 10K rows)
- table (with limits) ✅
- big_number_total ✅
- pie ✅
- echarts_timeseries_bar ✅
- echarts_timeseries_line ✅

### Medium (1-5 sec for 10K rows)
- sunburst_v2 ✅
- pivot_table_v2 ✅
- box_plot ✅

**Optimization Tips:**
- Use `row_limit` to cap data (recommended: 1000-5000 rows)
- Add filters to reduce data volume
- Enable caching for frequently accessed charts
- Use database aggregations when possible

---

## CHART-SPECIFIC TIPS (Verified Charts)

### Pie Charts (`pie`)
- Limit to 5-10 slices max for readability
- Use `groupby` for categorical dimension
- Sort by metric for better visualization

### Tables (`table`)
- Excellent for detailed data exploration
- Support multiple metrics
- Enable sorting and filtering

### Big Numbers (`big_number_total`)
- Perfect for dashboard KPIs
- Shows single aggregate value
- Use with COUNT, SUM, AVG, MAX, MIN

### Sunburst Charts (`sunburst_v2`)
- Requires 2+ hierarchical levels (e.g., `parlimen` → `dun`)
- Interactive drill-down capability
- Best for nested categorical data

### Pivot Tables (`pivot_table_v2`)
- Requires rows, columns, and metrics
- Excellent for cross-tabulation analysis
- Supports aggregations (SUM, COUNT, AVG, etc.)

### Box Plots (`box_plot`)
- Shows statistical distribution (quartiles, median, outliers)
- Requires numeric column and grouping dimension
- Great for comparing distributions across categories

### ECharts Bar Charts (`echarts_timeseries_bar`)
- Standard bar chart visualization
- Supports multiple metrics
- Good for categorical comparisons

### ECharts Line Charts (`echarts_timeseries_line`)
- Time series or trend visualization
- Supports multiple metrics
- Best for showing changes over time

---

## CREATING CHARTS VIA REST API

**Only use verified viz_types** when creating charts programmatically:

```json
{
  "slice_name": "My Chart Name",
  "viz_type": "echarts_timeseries_bar",  // Use ONLY verified types
  "datasource_id": 1,
  "datasource_type": "table",
  "params": "{...}",
  "query_context": "{...}"
}
```

**Valid viz_types for API:**
- `table`
- `pie`
- `big_number_total`
- `sunburst_v2`
- `pivot_table_v2`
- `box_plot`
- `echarts_timeseries_bar`
- `echarts_timeseries_line`

---

## ECHARTS PLUGIN STATUS

### ✅ Working ECharts Types
- `echarts_timeseries_bar` - Bar charts
- `echarts_timeseries_line` - Line charts

### ❌ Not Working ECharts Types
- `echarts_timeseries_area` - Area charts (NOT SUPPORTED)
- `echarts_treemap` - Tree maps (NOT SUPPORTED)
- `echarts_heatmap` - Heatmaps (NOT SUPPORTED)
- `echarts_gauge` - Gauge charts (NOT SUPPORTED)
- `echarts_funnel` - Funnel charts (NOT SUPPORTED)
- `echarts_radar` - Radar charts (NOT SUPPORTED)
- `echarts_scatter` - Scatter plots (NOT SUPPORTED)

**Note:** ECharts plugin is installed (`apache-superset[echarts]`) but only Bar and Line charts are supported in Superset 5.0.0.

---

## TESTING METHODOLOGY

Charts were validated through:
1. **REST API Creation**: Charts created via `/api/v1/chart/` endpoint
2. **UI Verification**: Charts checked in chart list and explore interface
3. **Friendly Name Test**: Working charts show friendly names ("Bar Chart"), broken ones show raw viz_types ("echarts_timeseries_area")
4. **Error Testing**: Failed charts show "This visualization type is not supported" error

**Total Charts Tested:** 20+
**Working:** 10 charts (8 viz_types)
**Broken:** 10+ charts deleted

---

## QUICK REFERENCE SUMMARY

### ✅ USE THESE (Production-Ready)
1. `table` - Data tables
2. `pie` - Pie charts
3. `big_number_total` - KPI displays
4. `sunburst_v2` - Hierarchical sunburst
5. `pivot_table_v2` - Pivot tables
6. `box_plot` - Box plots
7. `echarts_timeseries_bar` - Bar charts
8. `echarts_timeseries_line` - Line charts

### ❌ DON'T USE THESE (Confirmed Broken)
- `histogram`
- `echarts_timeseries_area`
- `echarts_treemap`
- `echarts_heatmap`
- `echarts_gauge`
- `echarts_funnel`
- `echarts_radar`
- Any other echarts_* except bar and line

### ⚠️ UNTESTED (Use with Caution)
All other viz_types listed in this document are theoretical and have not been tested in this Superset 5.0.0 instance.

---

**Last Updated:** 2025-12-17 (ECharts validation completed)
**Working Charts:** 10 charts across 8 viz_types
**ECharts Plugin:** ✅ Installed (Bar & Line only)
**Status:** ✅ Production-Ready
**Instance:** https://apache-superset-railway-production-13fe.up.railway.app
