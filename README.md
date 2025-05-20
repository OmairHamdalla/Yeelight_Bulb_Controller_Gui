# 💡 Yeelight Bulb Controller

A CustomTkinter-based GUI application for controlling Yeelight smart bulbs over your local network. This app allows you to easily connect to a bulb by entering its IP or auto-detecting it, and then control brightness, color modes, flows, and more...

<table>
<tr>
<td>

## Features
<ul>
  <li>Connect to Yeelight bulbs manually via IP or use auto-detection to brute-force search the IP</li>
  <li>Turn on/off the bulb</li>
  <li>Adjust brightness with a slider</li>
  <li>Set predefined modes: Study, Work, Rest</li>
  <li>Choose light's color from common preset of common colors</li>
  <li>Apply custom colors using the 3 RGB values</li>
  <li>Activate dynamic light flows (Breathing, Color Cycle, Pulse)</li>
</ul>

### Predefined Modes
<ul>
<li> Study Mode - Bright white for concentration
<li> Rest Mode - Warm, dim lighting
<li> Work Mode - Balanced, focused light
</ul>

### Light Flows
<ul>
<li> Breathing - Slowly fades into a color, then fades back to off 
<li> Color Cycle - Seamlessly fades from one color to the next
<li> Pulse - Flashes rapidly through different colors
</ul>



</td>
<td>

<img src="SS.png?raw=true" alt="SS"/>

</td>
</tr>
</table>


## Notes 
### IP Range & Auto Connection
-The Auto Connect feature scans your local IP range from 192.168.1.2 to 192.168.1.254 to find an active Yeelight bulb
-Your device and the bulb must be on the same Wi-Fi network for this to work

###  Customizing Flows and Modes
- Lighting flows are defined using the Flow class in the code as functions, You can customize flow effects by editing the properties of the flow object inside the script.
   - Change duration
   - RGB values
   - transition types
- Preset modes (Study, Rest, Work) are just pre-defined combinations of: 
   - Brightness
   - RGB Color
   - Temperature


## Dependencies
- [`yeelight`](https://pypi.org/project/yeelight/) - Python library to control Yeelight bulbs
- `customtkinter` - Modern UI for Tkinter
- `tkinter.messagebox` - For GUI dialogs
- Custom module: `IPConfig.py` (used for scanning LAN to detect bulb IPs)
   
Install the required packages:
```bash
pip install yeelight customtkinter
```
