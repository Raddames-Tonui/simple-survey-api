docker run -d \
  --name sky_survey_db \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=sky_survey_db \
  -p 5432:5432 \
  -v sky_survey_db:/var/lib/postgresql/data \
  postgres:15


docker exec -it sky_survey_db psql -U admin -c "CREATE DATABASE sky_survey_db;"


const csrfToken = Cookies.get("csrf_access_token");

fetch("/api/secure-endpoint", {
  method: "POST",
  credentials: "include", // important!
  headers: {
    "X-CSRF-TOKEN": csrfToken,
    "Content-Type": "application/json"
  },
  body: JSON.stringify(data)
});
