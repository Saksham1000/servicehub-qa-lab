# GraphQL Testing
Endpoint: `POST http://localhost:8000/graphql`. Run `pytest automation/graphql app/backend/tests/test_graphql.py -m graphql`.

```graphql
query FindServices($term: String) { services(search: $term) { id name category } }
```
Variables: `{"term":"mass"}`.

```graphql
{ providers { id name bio } }
```

Protected query (add `Authorization: Bearer <token>`):
```graphql
{ appointments { id customerId providerId serviceId status } }
```
Tests deliberately include unknown fields, malformed syntax, variables, filtering, missing authentication, and ownership scope. GraphQL commonly returns HTTP 200 with an `errors` array, so assert the envelope and data separately.
