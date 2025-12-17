# Superset REST API Reference

Complete REST API documentation for Apache Superset chart creation and management.

---

## Base URL

```
https://apache-superset-railway-production-13fe.up.railway.app
```

---

## Authentication

### Login Endpoint

**POST** `/api/v1/security/login`

Authenticate and obtain access token.

**Request:**
```json
{
  "username": "user@example.com",
  "password": "password",
  "provider": "db",
  "refresh": true
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Headers:**
- `Content-Type: application/json`

**cURL Example:**
```bash
curl -c cookies.txt -X POST "$BASE_URL/api/v1/security/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"password","provider":"db","refresh":true}'
```

---

### CSRF Token Endpoint

**GET** `/api/v1/security/csrf_token/`

Obtain CSRF token for POST/PUT/DELETE operations.

**Request Headers:**
- `Authorization: Bearer {access_token}`

**Response:**
```json
{
  "result": "IjkxZjUyOWI3NGJmOGI5NjUwOWNmOTQ4NDI1MzdmYzRhMTQwOTRlYjYi..."
}
```

**cURL Example:**
```bash
curl -b cookies.txt -c cookies.txt \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/security/csrf_token/"
```

**Important:** Must use cookies from login request.

---

## Chart Management

### List Charts

**GET** `/api/v1/chart/`

Retrieve list of all charts.

**Query Parameters:**
- `q`: URL-encoded query filter (optional)
- `page`: Page number (default: 0)
- `page_size`: Results per page (default: 20)

**Request Headers:**
- `Authorization: Bearer {access_token}`

**Response:**
```json
{
  "count": 5,
  "ids": [1, 2, 4, 5, 7],
  "result": [
    {
      "id": 2,
      "slice_name": "Parliamentary Constituency Distribution",
      "viz_type": "pie",
      "url": "/explore/?slice_id=2",
      "datasource_id": 1,
      "datasource_type": "table",
      "description": "Voter distribution across 14 parliamentary constituencies"
    }
  ]
}
```

**cURL Example:**
```bash
curl -b cookies.txt \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/chart/"
```

---

### Get Chart Details

**GET** `/api/v1/chart/{id}`

Retrieve detailed information for a specific chart.

**Path Parameters:**
- `id`: Chart ID (integer)

**Request Headers:**
- `Authorization: Bearer {access_token}`

**Response:**
```json
{
  "id": 2,
  "result": {
    "id": 2,
    "slice_name": "Parliamentary Constituency Distribution",
    "viz_type": "pie",
    "datasource_id": 1,
    "datasource_type": "table",
    "params": "{...JSON string...}",
    "query_context": "{...JSON string...}",
    "description": "Chart description",
    "cache_timeout": null,
    "owners": [...]
  }
}
```

**cURL Example:**
```bash
curl -b cookies.txt \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/chart/2"
```

---

### Create Chart

**POST** `/api/v1/chart/`

Create a new chart.

**Request Headers:**
- `Authorization: Bearer {access_token}`
- `Content-Type: application/json`
- `X-CSRFToken: {csrf_token}`
- `Referer: {base_url}/`

**Request Body:**
```json
{
  "slice_name": "Chart Name",
  "description": "Chart description (optional)",
  "viz_type": "pie",
  "datasource_id": 1,
  "datasource_type": "table",
  "params": "{...stringified JSON...}",
  "query_context": "{...stringified JSON...}",
  "cache_timeout": null,
  "owners": []
}
```

**Required Fields:**
- `slice_name`: Chart display name
- `viz_type`: Chart type identifier
- `datasource_id`: Dataset ID
- `datasource_type`: Usually "table"
- `params`: Chart configuration (JSON string)
- `query_context`: Query configuration (JSON string)

**Response (Success):**
```json
{
  "id": 8,
  "result": {
    "datasource_id": 1,
    "datasource_type": "table",
    "description": "Chart description",
    "params": "{...}",
    "slice_name": "Chart Name",
    "viz_type": "pie"
  }
}
```

**Response (Error):**
```json
{
  "errors": [
    {
      "message": "400 Bad Request: The CSRF session token is missing.",
      "error_type": "GENERIC_BACKEND_ERROR",
      "level": "error"
    }
  ]
}
```

**cURL Example:**
```bash
curl -b cookies.txt -c cookies.txt \
  -X POST "$BASE_URL/api/v1/chart/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $CSRF" \
  -H "Referer: $BASE_URL/" \
  -d '{
    "slice_name": "Test Chart",
    "viz_type": "table",
    "datasource_id": 1,
    "datasource_type": "table",
    "params": "{}",
    "query_context": "{}"
  }'
```

---

### Update Chart

**PUT** `/api/v1/chart/{id}`

Update an existing chart.

**Path Parameters:**
- `id`: Chart ID (integer)

**Request Headers:**
- `Authorization: Bearer {access_token}`
- `Content-Type: application/json`
- `X-CSRFToken: {csrf_token}`
- `Referer: {base_url}/`

**Request Body:**
Same as Create Chart, but all fields optional.

**Response:**
```json
{
  "id": 2,
  "result": {
    "slice_name": "Updated Chart Name",
    ...
  }
}
```

**cURL Example:**
```bash
curl -b cookies.txt -c cookies.txt \
  -X PUT "$BASE_URL/api/v1/chart/2" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $CSRF" \
  -H "Referer: $BASE_URL/" \
  -d '{
    "slice_name": "Updated Name"
  }'
```

---

### Delete Chart

**DELETE** `/api/v1/chart/{id}`

Delete a chart.

**Path Parameters:**
- `id`: Chart ID (integer)

**Request Headers:**
- `Authorization: Bearer {access_token}`
- `X-CSRFToken: {csrf_token}`
- `Referer: {base_url}/`

**Response:**
```json
{
  "message": "OK"
}
```

**cURL Example:**
```bash
curl -b cookies.txt -c cookies.txt \
  -X DELETE "$BASE_URL/api/v1/chart/8" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-CSRFToken: $CSRF" \
  -H "Referer: $BASE_URL/"
```

---

## Dataset Management

### List Datasets

**GET** `/api/v1/dataset/`

Retrieve list of available datasets.

**Response:**
```json
{
  "count": 1,
  "result": [
    {
      "id": 1,
      "table_name": "election_pahang",
      "schema": "sector2",
      "database": {
        "database_name": "ClickHouse Connect (Superset)",
        "id": 16
      }
    }
  ]
}
```

**cURL Example:**
```bash
curl -b cookies.txt \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/dataset/"
```

---

### Get Dataset Details

**GET** `/api/v1/dataset/{id}`

Retrieve dataset schema and column information.

**Response:**
```json
{
  "result": {
    "id": 1,
    "table_name": "election_pahang",
    "columns": [
      {
        "column_name": "parlimen",
        "type": "NULLABLE(STRING)",
        "groupby": true,
        "filterable": true
      },
      ...
    ],
    "metrics": [
      {
        "metric_name": "count",
        "expression": "COUNT(*)"
      }
    ]
  }
}
```

---

## Database Management

### List Databases

**GET** `/api/v1/database/`

Retrieve list of connected databases.

**Response:**
```json
{
  "count": 1,
  "result": [
    {
      "id": 16,
      "database_name": "ClickHouse Connect (Superset)",
      "backend": "clickhousedb",
      "allow_run_async": false,
      "expose_in_sqllab": true
    }
  ]
}
```

---

## Common Request Patterns

### Pattern 1: Complete Chart Creation Flow

```bash
#!/bin/bash
BASE_URL="https://apache-superset-railway-production-13fe.up.railway.app"
COOKIE_FILE="cookies.txt"

# 1. Login
curl -c "$COOKIE_FILE" -X POST "$BASE_URL/api/v1/security/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"pass","provider":"db","refresh":true}' \
  > login.json

TOKEN=$(cat login.json | jq -r '.access_token')

# 2. Get CSRF Token
CSRF=$(curl -s -b "$COOKIE_FILE" -c "$COOKIE_FILE" \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/security/csrf_token/" | jq -r '.result')

# 3. Create Chart
curl -b "$COOKIE_FILE" -c "$COOKIE_FILE" \
  -X POST "$BASE_URL/api/v1/chart/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $CSRF" \
  -H "Referer: $BASE_URL/" \
  -d '{...chart data...}'
```

---

### Pattern 2: List and Filter Charts

```bash
# Get all pie charts
curl -b cookies.txt \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/chart/?q=(filters:!((col:viz_type,opr:eq,value:pie)))"
```

---

### Pattern 3: Batch Operations

```bash
# Delete multiple charts
for id in 6 8 9; do
  curl -b cookies.txt -X DELETE \
    -H "Authorization: Bearer $TOKEN" \
    -H "X-CSRFToken: $CSRF" \
    "$BASE_URL/api/v1/chart/$id"
done
```

---

## Error Codes

| Status Code | Meaning | Common Cause |
|-------------|---------|--------------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Invalid JSON or parameters |
| 401 | Unauthorized | Invalid or expired token |
| 403 | Forbidden | Missing CSRF token or permissions |
| 404 | Not Found | Chart/dataset ID doesn't exist |
| 422 | Unprocessable Entity | Validation error in request |
| 500 | Internal Server Error | Server-side error |

---

## Common Error Messages

### "The CSRF session token is missing"

**Cause:** Missing cookies or CSRF token in request

**Solution:**
- Use `-b` and `-c` flags with cookie file
- Include `X-CSRFToken` header
- Include `Referer` header

### "Token has expired"

**Cause:** Access token expired (15 min default)

**Solution:**
- Re-authenticate to get fresh token
- Or use refresh token endpoint

### "Chart not found"

**Cause:** Invalid chart ID

**Solution:**
- List all charts to verify ID exists
- Check for typos in chart ID

---

## Rate Limiting

- **Default**: No explicit rate limiting
- **Recommended**: Max 100 requests/minute per user
- **Best Practice**: Cache responses when possible

---

## Response Formats

All responses are in JSON format.

### Success Response
```json
{
  "id": 2,
  "result": { ... }
}
```

### Error Response
```json
{
  "errors": [
    {
      "message": "Error description",
      "error_type": "ERROR_TYPE",
      "level": "error"
    }
  ]
}
```

---

## Headers Reference

### Required Headers for All Requests
- `Authorization: Bearer {access_token}`

### Required Headers for POST/PUT/DELETE
- `Content-Type: application/json`
- `X-CSRFToken: {csrf_token}`
- `Referer: {base_url}/`

### Cookie Management
- Use `-c` to save cookies
- Use `-b` to send cookies
- Store in file for session persistence

---

## Best Practices

1. **Cookie Management**
   - Always use persistent cookie file
   - Include `-b` and `-c` in all requests
   - Reuse cookie file across requests

2. **Token Handling**
   - Store access token securely
   - Refresh before expiration
   - Don't commit tokens to version control

3. **Error Handling**
   - Check response status codes
   - Parse error messages
   - Implement retry logic for 5xx errors

4. **Performance**
   - Reuse connections when possible
   - Cache chart metadata
   - Use filters to limit response size

5. **Security**
   - Use HTTPS only
   - Validate SSL certificates
   - Rotate credentials regularly

---

## Testing Endpoints

### Health Check
```bash
curl "$BASE_URL/health"
```

### API Version
```bash
curl "$BASE_URL/api/v1/"
```

---

## Related Documentation

- [Chart Creation Guide](../guides/superset_chart_creation_guide.md)
- [Chart Types Reference](../reference/superset_chart_types_reference.md)
- [Apache Superset API Docs](https://superset.apache.org/docs/api)

---

**Last Updated:** 2025-12-17
**API Version:** v1
**Superset Version:** 4.0+
