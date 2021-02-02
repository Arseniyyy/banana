def PID(Input, Feedback, SatUp, SatDwn, Kp, Ti, Kd, Proportional = 0, Differential = 0, Integral=0, dt = 0.0):
    #start_time = time.time()
    Proportional = Kp*(Input-Feedback)
    if dt == 0:
        Differential = 0
    else:
        Differential = Kd*(Input-Feedback)/dt
    #dt = time.time() - start_time
    Integral += (Input-Feedback)*dt/Ti
    if Integral > SatUp:
        Integral = SatUp
    else:
        if Integral < SatDwn:
           Integral = SatDwn
    Output = Proportional + Differential + Integral
    if Output > SatUp:
          Output = SatUp
    else:
        if Output < SatDwn:
           Output = SatDwn
    return Output, Proportional, Integral, Differential
