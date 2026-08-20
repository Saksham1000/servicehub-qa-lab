# API Testing
Start with `docker compose up --build -d`, then run `pytest automation/api -m api`. Import both files from `postman/`, select **ServiceHub Local**, and run the collection; CLI option: `newman run postman/ServiceHub.postman_collection.json -e postman/ServiceHub.local.postman_environment.json`. Requests cover positive contracts, validation, authentication, authorization, invalid resources, JSON types, and response-time sanity. FastAPI's interactive contract is at `http://localhost:8000/docs`. Tokens and generated IDs belong in environment variables, never committed secrets.

Registration intentionally returns account confirmation without a JWT. Call /api/auth/login separately to obtain a token; this mirrors the browser flow and ensures account creation does not silently authenticate the user.

