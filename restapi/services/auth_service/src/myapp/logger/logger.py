from gpylib.log4 import DEBUG, ERROR, INFO, WARN, Log4

# Go의 var Log *goglib.OLog2 = goglib.InitLogEnv(...) 에 대응하는 전역 로그 객체.
# api, service, repository 등 모든 패키지에서 아래와 같이 임포트하여 사용한다.
#
#   from src.logger.logger import log
#
#   log.info("user created: {}", username)
#   log.error("query failed: {}", str(e))

log = Log4("./bin/log", "auth", level=DEBUG, stdout=True)

__all__ = ["log", "DEBUG", "INFO", "WARN", "ERROR"]
