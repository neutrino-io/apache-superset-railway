# Validated Chart Types - Superset Instance

**Validation Date:** 2025-12-17
**Superset Instance:** https://apache-superset-railway-production-13fe.up.railway.app
**Validation Method:** UI inspection + API verification + Existing charts analysis

---

## ✅ VERIFIED WORKING (Production-Tested)

These chart types have been successfully created and are currently in use on the instance:

| Chart Name | `viz_type` | Category | Chart ID | Notes |
|------------|------------|----------|----------|-------|
| **Sunburst Chart** | `sunburst_v2` | Hierarchical | 1 | Multi-level hierarchy visualization |
| **Table** | `table` | Tabular | 4, 7 | Multiple working instances |
| **Big Number** | `big_number_total` | KPI | 5 | Single metric display |
| **Pie Chart** | `pie` | Part-to-Whole | 2 | Percentage breakdowns |

---

## 📊 AVAILABLE CHART TYPES (UI Confirmed)

All chart types available in the Superset UI as of 2025-12-17:

### Basic Charts (Easy to Use)

| Chart Name | Estimated `viz_type` | Category | Requirements |
|------------|---------------------|----------|--------------|
| **Area Chart** | `echarts_area` or `area` | Evolution | Time series data |
| **Bar Chart** | `echarts_timeseries_bar` | Ranking | Categorical data |
| **Line Chart** | `echarts_timeseries_line` | Evolution | Time series data |
| **Scatter Plot** | `scatter` | Correlation | X/Y numeric data |
| **Box Plot** | `box_plot` | Distribution | Numeric data |
| **Histogram** | `histogram` | Distribution | Single numeric column |

### KPI & Metrics

| Chart Name | Estimated `viz_type` | Category | Requirements |
|------------|---------------------|----------|--------------|
| **Big Number** | `big_number_total` | KPI | ✅ Single metric |
| **Big Number with Trendline** | `big_number` | KPI | Metric + time dimension |
| **Gauge Chart** | `echarts_gauge` | KPI | Single percentage metric |
| **Bullet Chart** | `bullet` | KPI | Actual vs target metrics |

### Advanced Statistical

| Chart Name | Estimated `viz_type` | Category | Requirements |
|------------|---------------------|----------|--------------|
| **Bubble Chart** | `echarts_bubble` | Correlation | X, Y, size metrics |
| **Radar Chart** | `echarts_radar` | Correlation | Multiple metrics |
| **Heatmap** | `heatmap` or `echarts_heatmap` | Correlation | Matrix data |
| **Calendar Heatmap** | `cal_heatmap` | Evolution | Time series data |
| **Horizon Chart** | `horizon` | Evolution | Dense time series |
| **Paired t-test Table** | `paired_ttest` | Table | Statistical analysis |
| **Parallel Coordinates** | `para` | Correlation | Multi-dimensional data |

### Flow & Relationship

| Chart Name | Estimated `viz_type` | Category | Requirements |
|------------|---------------------|----------|--------------|
| **Sankey Chart** | `echarts_sankey` | Flow | Source → Target flows |
| **Chord Diagram** | `chord` | Flow | Category relationships |
| **Graph Chart** | `graph_chart` | Flow | Network/node data |

### Hierarchical

| Chart Name | Estimated `viz_type` | Category | Requirements |
|------------|---------------------|----------|--------------|
| **Sunburst Chart** | `sunburst_v2` | Hierarchical | ✅ 2+ level hierarchy |
| **Treemap** | `echarts_treemap` | Hierarchical | 2+ level hierarchy |
| **Tree Chart** | `tree_chart` | Hierarchical | Parent-child relationships |
| **Partition Chart** | `partition` | Hierarchical | Cartodiagram style |

### Part of a Whole

| Chart Name | Estimated `viz_type` | Category | Requirements |
|------------|---------------------|----------|--------------|
| **Pie Chart** | `pie` | Part-to-Whole | ✅ Categorical breakdown |
| **Funnel Chart** | `echarts_funnel` | Flow | Sequential stages |
| **Nightingale Rose Chart** | `rose` | Part-to-Whole | Categorical with magnitude |
| **Waterfall Chart** | `waterfall` | Evolution | Cumulative changes |

### Tabular

| Chart Name | Estimated `viz_type` | Category | Requirements |
|------------|---------------------|----------|--------------|
| **Table** | `table` | Table | ✅ Any data |
| **Pivot Table** | `pivot_table_v2` | Table | Multi-dimensional data |
| **Time-series Table** | `time_table` | Table | Time series data |
| **Time-series Period Pivot** | `time_pivot` | Table | Time series comparison |

### Geographic (deck.gl)

**⚠️ All deck.gl charts require geographic coordinates (latitude/longitude)**

| Chart Name | Estimated `viz_type` | Requirements |
|------------|---------------------|--------------|
| **deck.gl Scatterplot** | `deck_scatter` | Lat/Lon points |
| **deck.gl Heatmap** | `deck_heatmap` | Lat/Lon density |
| **deck.gl 3D Hexagon** | `deck_hex` | Lat/Lon 3D aggregation |
| **deck.gl Arc** | `deck_arc` | Origin/Dest coordinates |
| **deck.gl Path** | `deck_path` | Line coordinates |
| **deck.gl Polygon** | `deck_polygon` | GeoJSON polygons |
| **deck.gl Geojson** | `deck_geojson` | GeoJSON features |
| **deck.gl Grid** | `deck_grid` | Lat/Lon grid |
| **deck.gl Screen Grid** | `deck_screengrid` | Lat/Lon screen-space |
| **deck.gl Contour** | `deck_contour` | Lat/Lon elevation |
| **deck.gl Multiple Layers** | `deck_multi` | Multiple layer types |
| **Country Map** | `country_map` | Country codes |
| **World Map** | `world_map` | Country data |
| **MapBox** | `mapbox` | Geographic data + MapBox token |

### Time Series Variations

| Chart Name | Estimated `viz_type` | Category | Requirements |
|------------|---------------------|----------|--------------|
| **Line Chart** | `echarts_timeseries_line` | Evolution | Time dimension |
| **Smooth Line** | `echarts_timeseries_smooth` | Evolution | Time dimension |
| **Stepped Line** | `echarts_timeseries_step` | Evolution | Time dimension |
| **Bar Chart** | `echarts_timeseries_bar` | Evolution | Time dimension |
| **Area Chart** | `echarts_timeseries_area` | Evolution | Time dimension |
| **Mixed Chart** | `mixed_timeseries` | Evolution | Multiple metric types |

### Custom/Advanced

| Chart Name | Estimated `viz_type` | Category | Requirements |
|------------|---------------------|----------|--------------|
| **Handlebars** | `handlebars` | Other | HTML/Handlebars knowledge |
| **Generic Chart** | `generic` | Other | Custom D3/JS code |
| **Word Cloud** | `word_cloud` | Other | Text data |

---

## ⚠️ DEPRECATED CHARTS (Do Not Use)

These chart types appear in the UI but are marked as DEPRECATED:

| Chart Name | Status | Use Instead |
|------------|--------|-------------|
| **Bubble Chart (legacy)** | ❌ DEPRECATED | `echarts_bubble` |
| **Time-series Percent Change** | ❌ DEPRECATED | Custom calculation + time series chart |

---

## 📋 VALIDATION SUMMARY

### Total Charts Available
- **Total Chart Types:** 55+
- **Verified Working:** 4 (table, pie, big_number_total, sunburst_v2)
- **Deprecated:** 2
- **Available but Untested:** 49+

### Chart Categories
1. **Evolution** (8 charts) - Time series and trends
2. **Ranking** (3 charts) - Comparisons and rankings
3. **Part-to-Whole** (4 charts) - Proportions and breakdowns
4. **Correlation** (6 charts) - Relationships and patterns
5. **Distribution** (4 charts) - Statistical distributions
6. **Flow** (3 charts) - Process flows and relationships
7. **Hierarchical** (4 charts) - Multi-level structures
8. **KPI** (4 charts) - Key performance indicators
9. **Table** (4 charts) - Tabular displays
10. **Map** (14 charts) - Geographic visualizations
11. **Other** (3 charts) - Custom and specialized

### Dataset Compatibility (sector2.election_pahang)

**✅ Highly Suitable Charts:**
- Table - Display raw voter data
- Pie Chart - Religious/constituency breakdowns
- Bar Chart - District/constituency comparisons
- Sunburst - Multi-level geography (Parlimen → DUN → Daerah)
- Treemap - Hierarchical population distribution
- Big Number - Total voter count KPIs
- Histogram - Age distribution
- Box Plot - Age statistics by region
- Pivot Table - Multi-dimensional analysis

**⚠️ Not Suitable (Missing Required Data):**
- All deck.gl charts - No lat/lon coordinates in dataset
- MapBox - No geographic coordinates
- Sankey - No flow/source-target data
- Graph Chart - No network/node relationships

**📊 Recommended Chart Types for Electoral Data:**

| Use Case | Recommended Charts | Priority |
|----------|-------------------|----------|
| Voter totals by constituency | Pie, Bar Chart | ✅ High |
| Age distribution | Histogram, Box Plot | ✅ High |
| Religious breakdown | Pie, Sunburst | ✅ High |
| Multi-level geography | Sunburst, Treemap | ✅ High |
| Dashboard KPIs | Big Number | ✅ High |
| Detailed data tables | Table, Pivot Table | ✅ High |
| Gender distribution | Pie Chart | Medium |
| District comparisons | Bar Chart, Treemap | Medium |

---

## 🧪 TESTING RECOMMENDATIONS

### Priority 1 - High Value Charts
Test these chart types next as they work well with electoral data:
1. **Bar Chart** (`echarts_timeseries_bar`) - Constituency comparisons
2. **Histogram** (`histogram`) - Age distribution
3. **Treemap** (`echarts_treemap`) - Hierarchical visualization
4. **Pivot Table** (`pivot_table_v2`) - Multi-dimensional analysis
5. **Box Plot** (`box_plot`) - Age statistics

### Priority 2 - Enhanced Visualizations
6. **Funnel Chart** (`echarts_funnel`) - Registration funnel
7. **Gauge Chart** (`echarts_gauge`) - Turnout percentages
8. **Radar Chart** (`echarts_radar`) - Multi-metric profiles
9. **Heatmap** (`echarts_heatmap`) - Correlation matrix
10. **Waterfall Chart** (`waterfall`) - Population changes

### Priority 3 - Advanced Analytics
11. **Sankey** - If flow data can be derived
12. **Graph Chart** - If relationship data available
13. **Word Cloud** - If text data available

---

## 🔍 VALIDATION METHODOLOGY

This document was created using:

1. **UI Inspection** - Browsed chart creation interface at `/chart/add`
2. **API Analysis** - Retrieved existing charts via `/api/v1/chart/`
3. **Production Verification** - Confirmed 4 chart types actively in use:
   - Chart #1: Sunburst (Parliment to DUN Voters)
   - Chart #2: Pie (Parliamentary Constituency Distribution)
   - Chart #4: Table (Religion Distribution Statistics)
   - Chart #5: Big Number (Total Registered Voters)
   - Chart #7: Table (District Voter Distribution)

4. **Documentation Cross-Reference** - Validated against:
   - `docs/reference/superset_chart_types_reference.md`
   - `docs/guides/superset_chart_creation_guide.md`

---

## 📝 NOTES

### viz_type Value Determination
- **Confirmed** viz_types are from actual working charts via API
- **Estimated** viz_types are based on:
  - Documentation patterns
  - Superset naming conventions
  - ECharts integration patterns
  - Common Superset implementations

### Testing Status Legend
- ✅ **Verified Working** - Successfully created and rendering
- 📊 **Available** - Visible in UI, not yet tested
- ⚠️ **Requires Data** - Needs specific data structure
- ❌ **Deprecated** - Marked deprecated in UI

### Next Steps
1. Test Priority 1 charts with electoral dataset
2. Document successful chart creation parameters
3. Update verified working list
4. Create chart creation examples for each type
5. Build decision tree for chart selection

---

**Last Updated:** 2025-12-17
**Validated By:** Claude Code (Automated UI + API validation)
**Instance Version:** Apache Superset 4.0+
**Dataset:** sector2.election_pahang (1,048,540 voters)
