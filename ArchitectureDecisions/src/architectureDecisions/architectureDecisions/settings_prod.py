# --oauth keys--
oauth_consumer_key = 'sRCATR7PtlxjrhTGEmCWGLcXtwIa'
oauth_secret_key = 'Cy5uBJeQz_fkSBGoYKfvfqQfpv0a'
# --------------

# --authentication jwt api--
authenticatorAPI = "http://sr-docker-xp01.corp.cablevision.com.ar:8000"
# --------------------------

# --admin role--
adminGroup = "CABLEVISION\/Sistemas Arquitectura"
# --------------

# --hostname, port, protocol--#
hostname = "sisarqdec.corp.cablevision.com.ar"
port = "80"
protocol = "http"
login_url = protocol + "://" + hostname + ':' + port + "/login"
# -----------------------------
log_path = "/volume/log/"
LOG_FILENAME = log_path + "architecture-decisions.log"
