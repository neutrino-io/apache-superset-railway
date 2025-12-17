# Superset Chart Types - Quick Reference

## Complete Chart Type Catalog

Based on analysis of Apache Superset instance (as of 2025-12-17)

---

## ✅ VERIFIED WORKING (Tested via REST API)

| Chart Name | viz_type | Category | Complexity | Best For |
|------------|----------|----------|------------|----------|
| Table | `table` | Tabular | ⭐ Easy | Raw data, multiple metrics |
| Pie Chart | `pie` | Part-to-Whole | ⭐ Easy | Percentage breakdowns |
| Big Number | `big_number_total` | KPI | ⭐ Easy | Single metric display |
| Sunburst | `sunburst_v2` | Hierarchical | ⭐⭐ Medium | Multi-level hierarchies |

---

## 📊 BASIC CHARTS (Recommended)

| Chart Name | viz_type | Category | Best For |
|------------|----------|----------|----------|
| Area Chart | `echarts_area` or `area` | Trend | Time series with magnitude |
| Bar Chart | `echarts_timeseries_bar` | Comparison | Categorical comparisons |
| Line Chart | `echarts_timeseries_line` | Trend | Trends over time |
| Bubble Chart | `echarts_bubble` | Multi-dimensional | 3D data (x, y, size) |
| Bullet Chart | `bullet` | Comparison | Goal vs actual |
| Funnel Chart | `echarts_funnel` | Flow | Conversion analysis |
| Histogram | `histogram` | Distribution | Frequency distribution |
| Box Plot | `box_plot` | Statistical | Distribution & outliers |

---

## 📈 ADVANCED STATISTICAL

| Chart Name | viz_type | Category | Best For |
|------------|----------|----------|----------|
| Gauge Chart | `echarts_gauge` | KPI | Progress/percentage |
| Radar Chart | `echarts_radar` | Multi-variable | Profile comparison |
| Heatmap | `heatmap` or `echarts_heatmap` | Density | Correlation matrix |
| Calendar Heatmap | `cal_heatmap` | Temporal | Activity patterns |
| Horizon Chart | `horizon` | Trend | Dense time series |

---

## 🔀 FLOW & RELATIONSHIP

| Chart Name | viz_type | Category | Best For |
|------------|----------|----------|----------|
| Sankey Diagram | `echarts_sankey` | Flow | Resource allocation |
| Chord Diagram | `chord` | Flow | Category relationships |
| Graph Chart | `graph_chart` | Network | Node relationships |

---

## 🌳 HIERARCHICAL

| Chart Name | viz_type | Category | Best For |
|------------|----------|----------|----------|
| Treemap | `echarts_treemap` | Hierarchical | Size comparison |
| Sunburst | `sunburst_v2` | Hierarchical | Multi-level drill-down |
| Partition | `partition` | Hierarchical | Cartodiagram style |

---

## 🗺️ GEOGRAPHIC (deck.gl)

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

---

## 📋 TABULAR

| Chart Name | viz_type | Category | Best For |
|------------|----------|----------|----------|
| Table | `table` | Tabular | Raw data display |
| Pivot Table | `pivot_table_v2` | Tabular | Multi-dimensional |

---

## 🎨 CUSTOM/ADVANCED

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
| Bubble (legacy) | N/A | Marked deprecated in UI | `echarts_bubble` |
| Legacy bubble | Old bubble type | Superseded | `echarts_bubble` |

---

## CHART SELECTION DECISION TREE

```
START: What data do you have?

├─ Geographic coordinates?
│  ├─ Points → deck_scatter
│  ├─ Density → deck_heatmap or deck_hex
│  ├─ Regions → deck_polygon
│  └─ Flows → deck_arc

├─ Time series?
│  ├─ Line trend → echarts_timeseries_line
│  ├─ Area trend → echarts_timeseries_area
│  ├─ Bars over time → echarts_timeseries_bar
│  └─ Dense data → horizon

├─ Single metric?
│  ├─ Just number → big_number_total
│  ├─ With progress → echarts_gauge
│  └─ With trend → big_number (with trendline)

├─ Categories to compare?
│  ├─ Simple bars → echarts_timeseries_bar
│  ├─ Part of whole → pie
│  └─ Sequential funnel → echarts_funnel

├─ Hierarchy (2+ levels)?
│  ├─ Nested circles → sunburst_v2
│  └─ Rectangles → echarts_treemap

├─ Distribution analysis?
│  ├─ Frequency → histogram
│  ├─ Statistical → box_plot
│  └─ Density → echarts_heatmap

├─ Relationships/Flow?
│  ├─ Node network → graph_chart
│  ├─ Flow between → echarts_sankey
│  └─ Category links → chord

├─ Multi-variable comparison?
│  └─ Profile → echarts_radar

└─ Raw data/tables?
   ├─ Simple → table
   └─ Pivot → pivot_table_v2
```

---

## COMPLEXITY RATINGS

### ⭐ Easy (Beginner-Friendly)
- table
- pie
- big_number_total
- echarts_timeseries_bar
- echarts_timeseries_line

### ⭐⭐ Medium (Some Configuration)
- sunburst_v2
- echarts_area
- histogram
- box_plot
- pivot_table_v2
- echarts_funnel
- echarts_gauge

### ⭐⭐⭐ Advanced (Complex Setup)
- deck.gl charts (require coordinates)
- echarts_sankey (requires source/target)
- graph_chart (requires node/edge data)
- handlebars (requires template knowledge)
- echarts_radar (requires multiple metrics)

---

## FEATURE MATRIX

| Chart Type | Multiple Metrics | Drill Down | Filters | Time Support | Export |
|------------|------------------|------------|---------|--------------|--------|
| table | ✅ | ✅ | ✅ | ✅ | ✅ |
| pie | ❌ | ✅ | ✅ | ❌ | ✅ |
| big_number_total | ❌ | ❌ | ✅ | ❌ | ✅ |
| sunburst_v2 | ❌ | ✅ | ✅ | ❌ | ✅ |
| echarts_timeseries_* | ✅ | ✅ | ✅ | ✅ | ✅ |
| deck_* | ❌ | ❌ | ✅ | ❌ | ⚠️ |
| pivot_table_v2 | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## COMMON USE CASES → CHART MAPPING

| Use Case | Primary Choice | Alternative |
|----------|----------------|-------------|
| Dashboard KPI | big_number_total | echarts_gauge |
| Sales by region | echarts_timeseries_bar | pie |
| User demographics | pie | echarts_treemap |
| Website traffic over time | echarts_timeseries_line | echarts_area |
| Conversion funnel | echarts_funnel | echarts_sankey |
| Geographic heatmap | deck_heatmap | deck_hex |
| Age distribution | histogram | box_plot |
| Multi-metric comparison | table | pivot_table_v2 |
| Organizational hierarchy | sunburst_v2 | echarts_treemap |
| Network analysis | graph_chart | echarts_sankey |
| Seasonal patterns | cal_heatmap | echarts_heatmap |
| Store locations | deck_scatter | country_map |
| Budget allocation | echarts_sankey | echarts_treemap |
| Performance metrics | echarts_radar | table |

---

## DATA REQUIREMENTS BY CHART TYPE

### Minimal Requirements (Any table works)
- table
- big_number_total

### Requires Categories
- pie (1 dimension)
- echarts_timeseries_bar (1 dimension)
- histogram (1 numeric column)

### Requires Hierarchy (2+ levels)
- sunburst_v2
- echarts_treemap
- partition

### Requires Coordinates
- deck_scatter (lat/lon)
- deck_heatmap (lat/lon)
- deck_hex (lat/lon)
- deck_arc (origin + dest lat/lon)
- deck_polygon (GeoJSON)

### Requires Network Data
- graph_chart (nodes + edges)
- chord (source + target categories)

### Requires Flow Data
- echarts_sankey (source, target, value)

---

## PERFORMANCE CONSIDERATIONS

### Fast (< 1 sec for 10K rows)
- table (with limits)
- big_number_total
- pie
- echarts_timeseries_bar

### Medium (1-5 sec for 10K rows)
- sunburst_v2
- pivot_table_v2
- echarts_heatmap

### Slow (> 5 sec for 10K rows)
- deck.gl charts (WebGL overhead)
- Complex hierarchical charts
- Heavy aggregations

**Optimization Tips:**
- Use row_limit to cap data
- Add filters to reduce data volume
- Enable caching for frequently accessed charts
- Use materialized views for complex queries

---

## CHART-SPECIFIC TIPS

### Pie Charts
- Limit to 5-10 slices max
- Use `show_labels_threshold` to hide tiny slices
- Sort by metric for better readability

### Tables
- Enable `show_cell_bars` for visual comparison
- Use `percent_metrics` for relative values
- Limit columns to avoid horizontal scroll

### Big Numbers
- Use subheader for context
- Choose appropriate number format
- Consider color for status indication

### deck.gl Charts
- Require geographic coordinates
- Best for > 1000 points
- May need MapBox API key

### Hierarchical Charts
- Keep hierarchy levels to 2-3 max
- Ensure child items sum to parent
- Use meaningful level names

---

**Last Updated:** 2025-12-17
**Source:** Apache Superset 4.0+ Analysis
