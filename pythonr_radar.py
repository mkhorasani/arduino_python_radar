import serial                                           
import serial
import streamlit as st
import plotly.graph_objects as go
import time

arduino = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS) #Change COM3 to whichever COM port your arduino is in

st.sidebar.title('Radar')
info_bar = st.empty()
info_1 = st.empty()
info_2 = st.empty()
radar_placeholder = st.empty()

r = [0]*180

theta = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34,
36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70,72,
74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104,106, 108,
110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132,134, 136, 138,
140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160,162, 164, 166, 168,
170, 172, 174, 176, 178, 180, 182, 184, 186, 188,190, 192, 194, 196, 198,
200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228,
230, 232, 234, 236, 238, 240, 242, 244, 246, 248, 250, 252, 254, 256, 258,
260, 262, 264, 266, 268, 270, 272, 274, 276, 278, 280, 282, 284, 286, 288,
290, 292, 294, 296, 298, 300, 302, 304, 306, 308, 310, 312, 314, 316, 318,
320, 322, 324, 326, 328, 330, 332, 334, 336, 338, 340, 342, 344, 346, 348,
350, 352, 354, 356, 358]

def radar_gauge(val,pos,placeholder):
    fig = go.Figure()
    pos = int(int(pos)/2)
    r[pos] = val

    fig.add_trace(go.Scatterpolar(
          r=r,
          theta=theta
    ))

    r2 = [0]*180
    r2[pos] = 1500
    fig.add_trace(go.Scatterpolar(
          r=r2,
          theta=theta
    ))

    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 1500]
        ),
      ),
      showlegend=False
    )
    placeholder.write(fig)

if st.sidebar.button('Start radar'):
    info_bar.info('Radar started')

    try:
        arduino.open()
    except:
        pass

    if st.sidebar.button('Stop radar'):
        info_bar.warning('Radar stopped')
        try:
            arduino.close()
        except:
            pass

    while True:
        arduino.flushInput()
        arduino.flushOutput()
        arduino.flush()
        try:
            val = arduino.readline().decode().strip('\r\n').split('*')[1]
        except:
            val = 0
        pos = arduino.readline().decode().strip('\r\n').split('*')[0]
        info_1.info(('Range (mm) = **%s**' % (val)))
        info_2.info(('Position (°) = **%s**' % (pos)))
        radar_gauge(val,pos,radar_placeholder)
        time.sleep(0.05)

info_bar.warning('Radar stopped')

try:
    arduino.close()
except:
    pass
