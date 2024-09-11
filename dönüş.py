import time
import numpy as np
from vehicle import Driver

# PID kontrolcüsü
def pid_controller(error, prev_error, total_error, dt):
    Kp = 0.1  # Daha düşük değerler deneyin
    Ki = 0.05
    Kd = 0.01

    P = Kp * error
    I = Ki * total_error
    D = Kd * (error - prev_error) / dt
    return P + I + D

# Fonksiyon: Tabelaya göre aracın yönlendirilmesi
def adjust_steering_based_on_sign(error, prev_error, total_error, last_time, driver):
    current_time = time.time()
    dt = current_time - last_time
    if dt == 0:  # Zaman farkı sıfır olduğunda PID'yi atla
        return total_error, current_time

    total_error += error * dt
    steering_adjustment = pid_controller(error, prev_error, total_error, dt)

    # Direksiyon açısını PID çıktısına göre ayarla
    steering_adjustment = np.clip(steering_adjustment, -1, 1)  # Limitleri kontrol et
    driver.setSteeringAngle(steering_adjustment)

    return total_error, current_time

def has_completed_turn(angle, target_angle, threshold=0.05):
    return abs(angle - target_angle) <= threshold

def start(detected_class,driver):
    driver.setCruisingSpeed(20)  # Sabit hız

    prev_error = 0
    total_error = 0
    last_time = time.time()
    turn_completed = True

    move_straight_time = 2
    wait_after_turn_time = 2

    if int(detected_class) == 7:  # Sola dönüş
        error = -1
        target_angle = -0.57
    elif int(detected_class) == 8:  # Sağa dönüş
        error = 1
        target_angle = 0.57
    elif int(detected_class) == 9:  # Düz git
        error = 0
        target_angle = 0
    
    start_time = time.time()
    while time.time() - start_time < move_straight_time:
        driver.setCruisingSpeed(20)
        driver.step()
        time.sleep(0.1)

    while turn_completed and driver.step() != -1:
        time.sleep(0.1)
        driver.setCruisingSpeed(25)
        total_error, last_time = adjust_steering_based_on_sign(error, prev_error, total_error, last_time, driver)

        # Aracın mevcut direksiyon açısını al
        current_angle = driver.getSteeringAngle()
        print(current_angle)
        # Eğer dönüş tamamlandıysa, PID kontrolünü durdur
        if has_completed_turn(current_angle, target_angle):
            turn_completed = False
            driver.setSteeringAngle(0)  # Direksiyon açısını sıfırla

    start_time_2 = time.time()
    while time.time() - start_time_2 < wait_after_turn_time:
        driver.setCruisingSpeed(20)
        driver.step()
        time.sleep(0.1)

    return 0