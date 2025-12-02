
timetable=[['Algorithms Lab (CSE Y3)  ,  CPL001', 'Algorithms Lab (CSE Y3)  ,  CPL001', 'Basic Electrical Lab  ,  BEE001', 'Basic Electrical Lab  ,  BEE001', 'Algorithms Lab (CSE Y3)  ,  CPL001', 'Algorithms Lab (CSE Y3)  ,  CPL001', 'Management and Economics  ,  NLC001'], ['Networks Lab (CSE Y3)  ,  CPL001', 'Networks Lab (CSE Y3)  ,  CPL001', 'Operating Systems (CSE Y3)  ,  NLC001', 'Environmental Studies  ,  NLC001', 'Management and Economics  ,  NLC001', 'Algorithms (CSE Y3)  ,  NLC001', 'Operating Systems (CSE Y3)  ,  NLC001'], ['Probability and Statistics  ,  NLC001', 'Environmental Studies  ,  NLC001', 'Management and Economics  ,  NLC001', 'Algorithms (CSE Y3)  ,  NLC001', 'Operating Systems (CSE Y3)  ,  NLC001', 'Probability and Statistics  ,  NLC001', 'Environmental Studies  ,  NLC001'], ['Management and Economics  ,  NLC001', 'Algorithms (CSE Y3)  ,  NLC001', 'Operating Systems (CSE Y3)  ,  NLC001', 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = "browser"   # ensures it opens zoomable


days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
slots = [f"Slot {i+1}" for i in range(len(timetable[0]))]

# convert zeros to empty string
display_data = [[("" if x == 0 else x) for x in row] for row in timetable]

fig = go.Figure(data=go.Table(
    header=dict(
        values=["Day"] + slots,
        fill_color="#1f77b4",
        font=dict(color='white', size=14),
        height=40
    ),
    cells=dict(
        values=[days] + list(zip(*display_data)),
        fill_color="white",
        height=35
    )
))

fig.update_layout(
    width=1200,        # 💥 Bigger view
    height=600,
)

fig.show()
