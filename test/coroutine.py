def accumulate():
    total = 0
    while True:
        value = yield total   # 밖에서 값을 받을 수도 있음
        total += value

gen = accumulate()
next(gen)        # 초기화
gen.send(10)     # total = 10
gen.send(20)     # total = 30
gen.send(5)      # total = 35