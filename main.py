radio.set_group(1)
radio.send_string("yeah")

charPos = 2
turn = False
gameOver = True
started = False
shot = False


#PairSend
def on_gesture_shake():
    global gameOver, started, turn
    if gameOver == True and started == False:
        pairId = randint(11, 100)
        print(pairId)
        radio.send_number(pairId)
        radio.set_group(pairId)  
        gameOver = False
        started = True
        led.plot(charPos, 4)
        turn = True


#ReceiveStr
def on_received_string(receivedString):
    global gameOver
    if receivedString == "Hit":
        gameOver = True
        basic.show_string("You Win")
        control.reset()

#ReceiveNum
def on_received_number(receivedNumber):
    global turn, charPos, gameOver, started, shot
    
    #ReceiveBullet
    if receivedNumber < 10:
        turn = False
        for i, in range(0, 6):
            if i != 5:
                led.plot(receivedNumber, i)
                led.unplot(receivedNumber, i - 1)
                pause(100)
            else:
                led.unplot(receivedNumber, i - 1)
                if receivedNumber == charPos:
                    gameOver = True
                    radio.send_string("Hit")
                    basic.show_string("You Lose")
                    control.reset()
    
        turn = True
        shot = False
    #ReceivePair
    else:
        if gameOver == True and started == False:
            radio.set_group(receivedNumber)
            print("paired")
            gameOver = False
            started = True
            led.plot(charPos, 4)


#Move Left
def on_button_pressed_a():
    global charPos, turn
    if turn == True and gameOver == False:
        if charPos > 0:
            led.unplot(charPos, 4)
            charPos = charPos - 1
            led.plot(charPos, 4)

#Move Right
def on_button_pressed_b():
    global charPos, turn
    if turn == True and gameOver == False:
        if charPos < 4:
            led.unplot(charPos, 4)
            charPos = charPos + 1
            led.plot(charPos, 4)

#Fire
def on_button_pressed_ab():
    global charPos, turn, shot

    if turn == True and gameOver == False and shot == False:
        shot = True
        for i, in range(0, 5):
            led.plot(charPos, 3 - i)
            if i != 0:
                led.unplot(charPos, 4 - i)
            pause(100)
        radio.send_number(charPos)


input.on_button_pressed(Button.A, on_button_pressed_a)
input.on_button_pressed(Button.B, on_button_pressed_b)
input.on_button_pressed(Button.AB, on_button_pressed_ab)
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

radio.on_received_number(on_received_number)


radio.on_received_string(on_received_string)
