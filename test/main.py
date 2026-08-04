import time

start_time = time.monotonic()
# 코드 실행
time.sleep(2)
end_time = time.monotonic()

print(f"start 시간: {start_time} 초")
print(f"end 시간: {end_time} 초")
print(f"경과 시간: {end_time - start_time} 초")
