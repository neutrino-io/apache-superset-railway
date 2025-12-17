# Railway Superset Documentation

Complete documentation for Apache Superset deployment with ClickHouse integration on Railway.

## 📚 Documentation Structure

```
docs/
├── README.md                           # This file - Documentation index
├── QUICKSTART.md                       # Quick start guide (5-minute setup)
├── CHANGES.md                          # Changelog and version history
│
├── setup/                              # Installation and configuration
│   └── clickhouse_setup.md             # ClickHouse driver setup guide
│
├── deployment/                         # Deployment guides and checklists
│   ├── deployment_guide.md             # Complete Railway deployment guide
│   └── deployment_checklist.md         # Pre/post-deployment checklist
│
├── troubleshooting/                    # Common issues and solutions
│   └── psycopg2_fix.md                 # PostgreSQL psycopg2 module fix
│
├── guides/                             # How-to guides and tutorials
│   └── superset_chart_creation_guide.md # REST API chart creation tutorial
│
├── reference/                          # Reference materials and quick lookups
│   └── superset_chart_types_reference.md # 40+ chart types catalog
│
└── api/                                # API documentation
    └── rest_api_reference.md           # Complete REST API reference
```

---

## 🚀 Quick Start

### New Users - Get Superset Running on Railway
1. **Quick Setup**: Start with [`QUICKSTART.md`](./QUICKSTART.md) for 5-minute setup
2. **Detailed Deployment**: See [`deployment/deployment_guide.md`](./deployment/deployment_guide.md)
3. **Setup ClickHouse**: Follow [`setup/clickhouse_setup.md`](./setup/clickhouse_setup.md)
4. **Verify Deployment**: Use [`deployment/deployment_checklist.md`](./deployment/deployment_checklist.md)

### AI Agents - Programmatic Chart Creation
1. **Authentication & Chart Creation**: Read [`guides/superset_chart_creation_guide.md`](./guides/superset_chart_creation_guide.md)
2. **Chart Type Selection**: Reference [`reference/superset_chart_types_reference.md`](./reference/superset_chart_types_reference.md)
3. **API Endpoints**: Check [`api/rest_api_reference.md`](./api/rest_api_reference.md)

### Troubleshooting Issues
- **PostgreSQL Connection Issues**: See [`troubleshooting/psycopg2_fix.md`](./troubleshooting/psycopg2_fix.md)
- **Chart Creation Errors**: Check [`guides/superset_chart_creation_guide.md#troubleshooting`](./guides/superset_chart_creation_guide.md)
- **Deployment Problems**: Review [`deployment/deployment_checklist.md`](./deployment/deployment_checklist.md)

---

## 📖 Documentation Overview

### 🎯 Getting Started

**[Quick Start Guide](./QUICKSTART.md)** *(5-minute setup)*
- Condensed Railway deployment guide
- Minimal configuration steps
- Essential commands only
- Fast path to running instance

**[Changes & Version History](./CHANGES.md)**
- Configuration changes summary
- Volume and storage updates
- PostgreSQL integration notes

---

### 🔧 Setup & Installation

**[ClickHouse Driver Setup](./setup/clickhouse_setup.md)**
- Dual driver installation (clickhouse-connect + clickhouse-driver)
- Connection string formats
- HTTP vs Native protocol
- Railway-specific configuration
- Testing database connectivity

**Key Features:**
- Support for both modern HTTP and native protocol drivers
- Connection examples for HTTP (port 8123) and Native (port 9440)
- Driver compatibility matrix
- Troubleshooting connection issues

---

### 🚀 Deployment

**[Complete Deployment Guide](./deployment/deployment_guide.md)**
- Architecture overview and component details
- Configuration files (railway.toml, Dockerfile, superset_config.py)
- Environment variables reference
- PostgreSQL metadata database setup
- Persistent volume configuration
- Health checks and monitoring
- Post-deployment verification
- Production best practices

**[Deployment Checklist](./deployment/deployment_checklist.md)**
- Pre-deployment requirements
- Database configuration steps
- Security configuration (secret keys, admin credentials)
- Environment variables verification
- Volume and storage setup
- Post-deployment validation
- Testing procedures
- Rollback procedures

**Key Sections:**
- Railway prerequisites
- Database setup and connection
- Security key generation
- Volume mounting for persistence
- Admin user creation
- Health check configuration

---

### 🩺 Troubleshooting

**[PostgreSQL psycopg2 Fix](./troubleshooting/psycopg2_fix.md)**
- "No module named 'psycopg2'" error resolution
- Python version detection and compatibility
- Package installation verification
- Force-reinstall procedures
- Database connectivity testing

**Problem Areas Covered:**
- Python version mismatches
- Hardcoded path issues
- Package installation failures
- Connection testing errors

---

### 📘 Usage Guides

**[Superset Chart Creation Guide](./guides/superset_chart_creation_guide.md)** *(20KB, 743 lines)*
- Complete REST API chart creation tutorial
- Authentication flow with cookie management
- 28+ chart type templates with working JSON examples
- Troubleshooting guide
- Best practices for AI agents
- Complete bash script examples

**Key Sections:**
- Prerequisites & Authentication
- Chart Creation Process
- Chart Structure Reference
- Available Chart Types (Detailed)
- Common Patterns (Metrics, Filters, Colors)
- Troubleshooting
- Complete Working Script

---

### 📚 Reference Materials

**[Chart Types Quick Reference](./reference/superset_chart_types_reference.md)** *(9.2KB, 316 lines)*
- Complete catalog of 40+ chart types
- Chart selection decision tree
- Complexity ratings (⭐ Easy, ⭐⭐ Medium, ⭐⭐⭐ Advanced)
- Use case mapping
- Feature matrix
- Performance considerations

**Key Sections:**
- Verified Working Charts (✅ Tested)
- Basic Charts (Recommended)
- Advanced Statistical Charts
- Geographic Visualizations (deck.gl)
- Flow & Relationship Charts
- Chart Selection Decision Tree
- Common Use Cases → Chart Mapping

---

### 🔌 API Documentation

**[REST API Reference](./api/rest_api_reference.md)** *(11.4KB)*
- Complete API endpoint documentation
- Authentication methods (JWT + CSRF)
- Chart CRUD operations (GET, POST, PUT, DELETE)
- Dataset and Database management
- Request/response formats
- Error codes and handling
- Common request patterns
- Best practices

**Endpoints Covered:**
- `/api/v1/security/login` - Authentication
- `/api/v1/security/csrf_token/` - CSRF token
- `/api/v1/chart/` - Chart management
- `/api/v1/dataset/` - Dataset operations
- `/api/v1/database/` - Database connections

---

## 🎯 Project Context

### System Overview
- **Superset Instance**: Apache Superset 4.0+ on Railway
- **Metadata Database**: PostgreSQL (user accounts, charts, dashboards)
- **Data Sources**: ClickHouse (sector2.election_pahang)
- **Data**: Pahang electoral demographics (1,048,540+ records)
- **Access**: REST API with JWT + CSRF authentication
- **Storage**: Persistent volumes for uploads and cache

### Dataset Information
- **Database ID**: 16 (ClickHouse Connect)
- **Dataset ID**: 1 (election_pahang)
- **Schema**: sector2
- **Records**: 1,048,540 voters
- **Columns**: 20 fields including demographics, location, religion

### Key Columns
- `parlimen` - Parliamentary constituency (14 constituencies)
- `dun` - State assembly constituency
- `daerah` - District (12 districts)
- `umur` - Age
- `agama` - Religion
- `date_lahir` - Date of birth
- Geographic data: `negeri`, `bandar`, `poskod`

---

## ✅ Verified Working Charts

Successfully created and tested via REST API:

| Chart ID | Name | Type | Description |
|----------|------|------|-------------|
| 1 | Parliment to DUN | `sunburst_v2` | Hierarchical view (existing) |
| 2 | Parliamentary Constituency Distribution | `pie` | 14 constituencies breakdown |
| 4 | Religion Distribution Statistics | `table` | Religion demographics |
| 5 | Total Registered Voters - Pahang | `big_number_total` | Total voters KPI |
| 7 | District Voter Distribution | `table` | Top 12 districts with percentages |

**Access URLs:**
- Superset: `https://apache-superset-railway-production-13fe.up.railway.app`
- Charts: `https://apache-superset-railway-production-13fe.up.railway.app/explore/?slice_id={id}`

---

## 🔧 Common Tasks

### Deploy Superset on Railway
```bash
# See: QUICKSTART.md or deployment/deployment_guide.md
# Quick steps:
1. Configure railway.toml with PostgreSQL connection
2. Generate secret keys
3. Set admin credentials
4. Deploy to Railway
5. Verify health checks
```

### Setup ClickHouse Connection
```bash
# See: setup/clickhouse_setup.md
# Connection formats:
HTTP:    clickhouse+http://user:pass@host:8123/database
Native:  clickhouse+native://user:pass@host:9440/database
```

### Create a New Chart via API
```bash
# See: guides/superset_chart_creation_guide.md
# Quick steps:
1. Authenticate (get token + CSRF + cookies)
2. Choose chart type from reference guide
3. Construct JSON payload
4. POST to /api/v1/chart/
```

### Select Chart Type
```bash
# See: reference/superset_chart_types_reference.md
# Use the decision tree:
- Geographic data? → deck.gl charts
- Time series? → echarts_timeseries_*
- Categories? → pie or bar
- Single metric? → big_number_total
- Hierarchy? → sunburst_v2
```

### Troubleshoot Deployment Issues
```bash
# See: troubleshooting/psycopg2_fix.md
# Common issues:
- psycopg2 errors → Check Python version compatibility
- Connection failures → Verify PostgreSQL connection string
- Volume issues → Check mount paths in railway.toml
```

### Troubleshoot Chart Creation Errors
```bash
# See: guides/superset_chart_creation_guide.md → Troubleshooting
# Common issues:
- CSRF error → Missing cookies
- Empty query → Invalid params
- Type not supported → Wrong viz_type
```

---

## 📊 Chart Type Quick Lookup

| Need | Chart Type | viz_type |
|------|------------|----------|
| Dashboard KPI | Big Number | `big_number_total` ✅ |
| Percentage breakdown | Pie Chart | `pie` ✅ |
| Data table | Table | `table` ✅ |
| Multi-level hierarchy | Sunburst | `sunburst_v2` ✅ |
| Bar comparison | Bar Chart | `echarts_timeseries_bar` |
| Age distribution | Histogram | `histogram` |
| Geographic density | Heatmap | `deck_heatmap` |

---

## 🔗 Related Resources

### Internal Documentation
- [Quick Start Guide](./QUICKSTART.md)
- [Deployment Guide](./deployment/deployment_guide.md)
- [ClickHouse Setup](./setup/clickhouse_setup.md)
- [Chart Creation Guide](./guides/superset_chart_creation_guide.md)
- [Chart Types Reference](./reference/superset_chart_types_reference.md)
- [API Reference](./api/rest_api_reference.md)

### External Resources
- [Apache Superset Documentation](https://superset.apache.org/docs/intro)
- [Superset REST API](https://superset.apache.org/docs/api)
- [Railway Documentation](https://docs.railway.app/)
- [ClickHouse Documentation](https://clickhouse.com/docs)
- [ECharts Documentation](https://echarts.apache.org/en/index.html)
- [deck.gl Documentation](https://deck.gl/)

---

## 📝 Contributing

When adding new documentation:

1. **Place in correct folder**:
   - Getting started → Root level (`QUICKSTART.md`, `CHANGES.md`)
   - Setup/installation → `setup/`
   - Deployment guides → `deployment/`
   - Troubleshooting → `troubleshooting/`
   - How-to guides → `guides/`
   - Reference materials → `reference/`
   - API docs → `api/`

2. **Update this README**:
   - Add entry in Documentation Overview
   - Update Quick Lookup tables if relevant
   - Add to appropriate Quick Start section

3. **Follow format**:
   - Use clear headings and structure
   - Include code examples with syntax highlighting
   - Add troubleshooting sections where applicable
   - Keep examples updated and tested
   - Include file sizes for large documents

---

## 📅 Last Updated

**Date**: 2025-12-17
**Superset Version**: 4.0+
**Documentation Status**: Complete & Active
**Total Documentation**: 60KB+ across 11 files

---

## 🎓 Learning Paths

### Path 1: Deploy Superset on Railway (New Users)
1. Read [QUICKSTART.md](./QUICKSTART.md) for overview
2. Follow [deployment/deployment_guide.md](./deployment/deployment_guide.md) step-by-step
3. Setup ClickHouse connection using [setup/clickhouse_setup.md](./setup/clickhouse_setup.md)
4. Verify deployment with [deployment/deployment_checklist.md](./deployment/deployment_checklist.md)
5. Troubleshoot issues with [troubleshooting/psycopg2_fix.md](./troubleshooting/psycopg2_fix.md)

### Path 2: Create Charts Programmatically (AI Agents/Developers)
1. Read [guides/superset_chart_creation_guide.md](./guides/superset_chart_creation_guide.md) for authentication
2. Choose chart type from [reference/superset_chart_types_reference.md](./reference/superset_chart_types_reference.md)
3. Use [api/rest_api_reference.md](./api/rest_api_reference.md) for API details
4. Test with simple table or pie chart first
5. Experiment with advanced chart types

### Path 3: Advanced Usage (Power Users)
1. Jump to [reference/superset_chart_types_reference.md](./reference/superset_chart_types_reference.md) for quick lookup
2. Use [api/rest_api_reference.md](./api/rest_api_reference.md) for endpoint details
3. Customize chart parameters as needed
4. Explore deck.gl charts for geographic data
5. Review [deployment/deployment_guide.md](./deployment/deployment_guide.md) for production optimization

---

## ⚡ Quick Commands

```bash
# Deployment
railway up                                    # Deploy to Railway
railway logs                                  # View deployment logs
railway open                                  # Open Superset in browser

# API Access
# View all charts
curl -b cookies.txt -H "Authorization: Bearer $TOKEN" \
  $SUPERSET_URL/api/v1/chart/

# Create chart from template
bash create_chart_script.sh

# Delete test chart
curl -b cookies.txt -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-CSRFToken: $CSRF" \
  $SUPERSET_URL/api/v1/chart/{id}
```

See the full guides for complete examples and explanations.
