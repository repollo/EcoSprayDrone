# EcoSprayDrone: **DIY AI-Powered Drone for Intelligent Weeding with Automated Battery Swap Station**

Empower farmers worldwide with AI-driven drones that specifically target weeds, eliminating the need to spray entire fields, resulting in fewer chemicals and reduced labor. This project combines precision drone flight with AI image classification and an innovative battery swapping mechanism, all made affordable and accessible.

## **Attribution and Purpose**
This project, EcoSprayDrone, was originally conceived and executed by the YouTube creator **NathanBuildsDIY**. I am not the original creator of this project. My aim in uploading it to GitHub is threefold:
- **Organize and Present**: I wanted to structure and present the rich content Nathan has created in a format that’s easy for the community to navigate and understand.
- **Conciseness**: While the original content is vast and valuable, I've made efforts to condense the information without losing its essence, making it more accessible for quick reading and reference.
- **Preservation**: GitHub is a platform known for its posterity and community contributions. By uploading it here, I hope to ensure that NathanBuildsDIY’s hard work remains available and can be built upon by the community for years to come.

I highly recommend checking out [NathanBuildsDIY's YouTube Channel](https://www.youtube.com/@nathanbuildsdiy) for detailed videos, his journey in creating the EcoSprayDrone, and more of his innovative projects.

Please ensure all contributions, feedback, and usage respect the original creator's intentions and rights.

## **Overview**
This drone uses AI to identify and selectively spray only the weeds in a field, significantly reducing the chemical usage while maintaining crop yields. The base station is designed to automatically swap and recharge the drone's battery and update its flight plan, minimizing human intervention. The goal is to ensure smallholding farmers benefit from cleaner and cost-effective agricultural practices.

The project is divided into three primary components:
1. **[Automated Drone Battery Swap and Landing Pad](#1-automated-drone-battery-swap-and-landing-pad)**
2. **[Autonomous Intelligent Drone Sprayer](#2-autonomous-intelligent-drone-sprayer)**
3. **[AI-powered Weeding Mechanism with Raspberry Pi](#3-ai-powered-weeding-mechanism-with-raspberry-pi)**

## **1. Automated Drone Battery Swap and Landing Pad**

- **Description**: A fully automated drone landing pad and battery swap station that doesn't require precision landing.
- **Tutorial Video**: [DIY automated drone battery swap, landing pad and relaunch](https://www.youtube.com/watch?v=Q7A3PlqpgYs)
- **Circuit Diagram and Code**:
  - ![Circuit Diagram](/Electronics_batteryswap.jpg)
  - [Controlled landing pad motors arduino file](/drone_battery_swap_full.ino)
  - [Make the arduino "wait" file](/donothing.ino)
  - [AutoIt file](/drone_autoit.au3)
- **Bill of Materials**: Detailed list with links to purchase materials [Excel File](/BOM.xlsx) or [Numbers File](/BOM.numbers).
  - ***Landing Pad:***

| Yes/No | Description                                                                                                      | Quantity | Amount  |
|--------|------------------------------------------------------------------------------------------------------------------|----------|---------|
| TRUE   | 4'x8 1/2" plywood                                                                                                | 2        | $36.00  |
| TRUE   | 2"x4"x8' lumber                                                                                                  | 8        | $24.00  |
| TRUE   | 2"x6"x8' lumber                                                                                                  | 2        | $11.00  |
| TRUE   | 2"x2"x8' lumber                                                                                                  | 6        | $17.00  |
| TRUE   | 1/2"x10' threaded rod                                                                                            | 3        | $40.00  |
| TRUE   | Makermotor 3/8" D Shaft 12V DC Reversible Electric Gear Motor 100 RPM (https://www.amazon.com/gp/product/B07...) | 3        | $240.00 |
| TRUE   | 1/2" course threaded nuts                                                                                        | 25       | $7.00   |
| TRUE   | 3" screws 5lb bucket                                                                                             | 1        | $23.00  |
| TRUE   | 50' roll 18-2 wire                                                                                               | 2        | $16.00  |
| TRUE   | container wire nuts                                                                                              | 1        | $10.00  |
| TRUE   | goop adhesive                                                                                                    | 1        | $5.00   |
| TRUE   | 4'x8 1/2" plywood                                                                                                | 1        | $18.00  |
| TRUE   | 2"x2"x8' lumber                                                                                                  | 6        | $17.00  |
| TRUE   | 14" linear actuator (https://www.amazon.com/gp/product/B07...)                                                   | 2        | $98.00  |
| TRUE   | 16" linear actuator (same link as above)                                                                         | 1        | $50.00  |
| TRUE   | 4" linear actuator (same link as above)                                                                          | 1        | $36.00  |
| TRUE   | 4s lipo battery charger (https://www.amazon.com/gp/product/B07...)                                               | 1        | $15.00  |
| TRUE   | roll thick copper tape (https://www.amazon.com/gp/product/B09...)                                                | 1        | $17.00  |
| TRUE   | 1" screws 1 lb container                                                                                         | 1        | $5.00   |
| TRUE   | 10A Cytron dual motor controller (ESC) (https://www.amazon.com/gp/product/B07...)                                | 4        | $96.00  |
| TRUE   | Arduino Uno (https://www.amazon.com/Arduino-A00006...)                                                           | 1        | $29.00  |
| TRUE   | 20A 12V power supply (https://www.amazon.com/gp/product/B07...)                                                  | 1        | $23.00  |
| TRUE   | Electrical power strip                                                                                           | 1        | $5.00   |
| TRUE   | Laptop (not included in price - use one you have)                                                                | 1        |         |
|        | Total                            |          | $838.00 |

- ***Drone:***

| Yes/No | Description                                                                           | Quantity | Amount  |
|--------|---------------------------------------------------------------------------------------|----------|---------|
| TRUE   | S500 frame Drone (https://www.amazon.com/gp/product/B01...)                           | 1        | $48.00  |
| TRUE   | 30A ESC (https://www.amazon.com/gp/product/B07...)                                    | 4        | $40.00  |
| TRUE   | 920kV drone motors (https://www.amazon.com/gp/product/B09...)                         | 4        | $40.00  |
| TRUE   | two-pair drone props                                                                  | 1        | $14.00  |
| TRUE   | Cube orange, 1 here 3+ GPS, 1 900MHz radio (https://irlock.com/collections/combos...) | 1        | $679.00 |
| TRUE   | tf-mini (lidar - optional) (https://irlock.com/collections/rangef...)                 | 1        | $50.00  |
| TRUE   | Balsa wood                                                                            | 1        | $10.00  |
| TRUE   | wood glue                                                                             | 1        | $5.00   |
| TRUE   | zip ties                                                                              | 1        | $5.00   |
| TRUE   | adhesive velcro                                                                       | 1        | $5.00   |
| TRUE   | 4s 5200 mAH lipo Battery (https://www.amazon.com/Zeee-Battery-5...)                   | 2        | $98.00  |
| TRUE   | liquid electrical tape                                                                | 1        | $5.00   |
|        | Total                                                                                 |          | $999.00 |


## **2. Autonomous Intelligent Drone Sprayer**

- **Description**: An intelligent drone capable of identifying and spraying specific weeds in a field.
- **Tutorial Video**: [DIY Autonomous Intelligent drone sprayer - Parts List, Schematics, Build Details](https://www.youtube.com/watch?v=Fflbc_y2IGQ)
- **Schematics and Code**:
  - [Electrical Schematic](/schematic_drone.pdf)
  - TensorFlow code files:
    - [webcamCapture.py](/webcamCapture.py)
    - [sprayerLoop_captureOnly.py](/sprayerLoop_captureOnly.py)
    - [BuildModel.py](/BuildModel.py)
    - [PredictImage.py](/PredictImage.py)
    - [listener_mpScriptsTab.py](/listener_mpScriptsTab.py)
    - [sprayerLoop.py](/sprayerLoop.py)
- **Bill of Materials**: A detailed list of components and their associated costs [Excel File](/BOM.xlsx) or [Numbers File](/BOM.numbers).
- ***Sprayer:***

| Yes/No | Description                                                                                                                       | Quantity | Amount |
|--------|-----------------------------------------------------------------------------------------------------------------------------------|----------|--------|
| TRUE   | L298N Motor Controller (https://www.amazon.com/Qunqi-Controll...)                                                                 | 1        | $7.00  |
| TRUE   | 12V and 5V DC buck converter (adjustable) (https://www.amazon.com/dp/B01MQGMOKI?...)                                              | 1        | $12.00 |
| TRUE   | Sprayer Pump (https://www.amazon.com/gp/product/B07...)                                                                           | 1        | $10.00 |
| TRUE   | Nozzle (https://www.amazon.com/Hourleey-Misti...)                                                                                 | 1        | $8.00  |
| TRUE   | Nozzle tubing (https://www.amazon.com/REDTRON-Distri...)                                                                          | 1        | $8.00  |
| TRUE   |   5' section of 1/2" PVC, 6 90 degree connectors, 4 T connectors, silicon, 1/4" inside diameter tubing - $25  (tank/landing gear) | 1        | $25.00 |
|        | Total                                             |          | $70.00 |

- ***Camera V2:***

| Yes/No | Description                                                                           | Quantity | Amount |
|--------|---------------------------------------------------------------------------------------|----------|--------|
| TRUE   | Raspberry Pi Zero 2 W (https://www.raspberrypi.com/products/...)                      | 1        | $15.00 |
| TRUE   | Raspberry Pi Camera 2 (https://www.raspberrypi.com/products/...)                      | 1        | $25.00 |
|        | Total |          | $40.00 |


## **3. AI-powered Weeding Mechanism with Raspberry Pi**

- **Description**: Implement AI for image classification to identify weeds and command the drone to spray them selectively.
- **Tutorial Video**: [DIY AI weed spraying drone, automatic landing pad/battery swap](https://www.youtube.com/watch?v=X9XkCe1RPQY)
- **Wiring and Scripts**:
  - [Wiring diagram for Raspberry Pi and Pump](/Electronics_rpi_pump.pdf)
  - Scripts: 
    - [takePhotos.py](/takePhotos.py)
    - [BuildModel_Quantized_Lite_ubuntu2.py](/BuildModel_Quantized_Lite_ubuntu2.py)
    - [droneSprayer_v1.py](/droneSprayer_v1.py)

## **Inspiration**
AI for image classification, precision drone flight, and automatic battery swaps are all attainable at reasonable prices. By making this prototype publicly available, we aim to inspire others to learn, improve, and ensure the benefits reach farmers worldwide, leading to less expensive, cleaner food production.

## **Alternatives and Further Reading**
A list of other similar projects and systems with their distinct features,

  - [Automated Battery Swap and Recharge...](https://dspace.mit.edu/handle/1721.1/81474) - requires precision landing
  - [Swap-it: the Autonomous Drone-battery...](https://www.youtube.com/watch?v=MTez24dTvq4) - requires operator to land, no instructions for build
  - [Battery Swap and Flight - Drone Base ...](https://www.youtube.com/watch?v=H6kvx94ddxU) - precision landing
  - [Autonomous drone battery replacementB...](https://www.youtube.com/shorts/HCztzRv4lN4) - robot arm/very expensive
  - [RAPID | Prototype for the Battery-Hot...](https://www.youtube.com/watch?v=kweZw4rbzXU) - precision landing

## **Feedback and Contribution**

Your feedback and contributions are invaluable to the continued improvement of this project. Here's how you can help:

- **Bug Reports and Feature Requests**: Encountered any bugs or would like to suggest a feature? Please [open an issue](https://github.com/repollo/EcoSprayDrone/issues) describing the problem or suggestion.

- **Documentation**: Improve our documentation by either correcting mistakes, adding clarifications, or even expanding on certain areas. Submit a pull request with your proposed changes.

- **Code Contribution**: If you'd like to contribute to the project's source code, fork the repository, make your changes, and then submit a pull request. For more detailed steps, view our [contribution guide](https://github.com/repollo/EcoSprayDrone/CONTRIBUTING.md).

## **TODO List**

1. **CONTRIBUTING.md**: Create the contributing instructions markdown file.
2. **Bash Scripts**: Develop scripts in Bash for automated installation of the necessary files.
3. **Refactoring**: Review and refactor the current codebase to enhance its maintainability, readability, and overall structure.
4. **Platform Development**: Explore opportunities to evolve the current codebase into a comprehensive platform, fostering an ecosystem that streamlines and manages all system interactions efficiently. ROS maybe?
5. **Integration with Other Agricultural Tools**: Explore how the EcoSprayDrone can be integrated with other farm machinery or tools for a comprehensive farming solution.
6. **Enhance AI Training Data**: Accumulate more diverse weed images to improve the AI's image classification accuracy.
7. **Expand Battery Swap Mechanism**: Design modifications to support multiple drone models and battery types.
8. **Safety Mechanisms**: Implement features to ensure drone safety in cases of malfunction or unexpected obstacles.
9. **Detailed Testing**: Ensure all components function as expected in various conditions (different terrains, weather conditions, etc.).
10. **Optimization**: Work on optimizing the code for faster response times and increased efficiency.
11. **Feedback Loop**: Create a system for users to provide feedback, report issues, or suggest enhancements.
12. **Expand Hardware Compatibility**: Test with various other hardware components to ensure a broader range of compatibility.
13. **Localization and Internationalization**: Translate project documentation and software interfaces to support non-English speaking users.
14. **Remote Monitoring**: Develop an application for farmers to remotely monitor the drone's operation, including battery levels, area covered, and potential issues.
15. **Expand the AI Model**: Train the model with more diverse data for better weed identification across different terrains and conditions.
16. **Documentation**: Regularly update the README and other documentation based on user feedback and technological advancements.
17. **Tutorials**: Create more detailed tutorials or workshops for different components, ensuring that even beginners can get started with ease.
18. **Environmental Impact Study**: Examine the long-term impact of the drone's usage on fields and the environment. This could encompass factors such as, the effects of the reduced use of chemicals (due to targeted spraying) on soil health and groundwater; the potential disturbance to local wildlife due to the drone's operations; carbon footprint of the drone compared to traditional farming machinery; the waste generated from used-up drone batteries and parts, and the recycling or disposal of these components.
19. **Temporal Environmental Monitoring**: Utilize the drone system for periodic landscape and waterbody imaging. Over time, the collected visual data can be compared to: track changes in terrain, vegetation cover, and water levels; detect early signs of algal blooms, eutrophication, or other ecological disturbances in water bodies; provide critical insights into rapid changes or shifts in local ecosystems. This data can be vital for first response teams, helping them to intervene promptly and possibly prevent larger environmental disasters; combine the visual data with other environmental parameters (like water temperature, nutrient levels) collected separately, to develop a comprehensive understanding of local environmental trends and how this affects larger global ecosystems.

## README and Documentation Improvements:

1. **Table of Contents**: Consider adding a table of contents at the beginning for easier navigation.
2. **Images**: If possible, incorporate images/screenshots of the actual drone, the landing pad, or any relevant component. Visuals can enhance understanding significantly.
3. **Quick Start or Getting Started Section**: This section can provide users with a set of steps to get the drone up and running quickly. It would be helpful for those who might want to test it before delving deep into the details.
4. **Safety Precautions**: Drones, especially ones equipped for spraying, can be potentially hazardous. A section dedicated to safety precautions, standards, passive/active design paradigms can be invaluable. Examples: 
   - Implementing a drone system, especially one equipped for spraying, necessitates thorough safety considerations. Recognizing the potential risks, we highly recommend adhering to rigorous safety precautions and guidelines. As a crucial suggestion, when setting up this drone system, ensure that its Landing Station is strategically placed away from residential areas and animals. Furthermore, aim to minimize or, if possible, eliminate the drone's overhead flight path to prevent potential hazards.
   - MSDS
   - Chemical storage and management
   - PPE
1. **FAQ Section**: Add a section for frequently asked questions. This can address common concerns or misconceptions.
2. **Collaboration and Contribution**: If you're open to collaboration or improvements from the community, detail how others can contribute.
3. **Versioning**: If this is a work in progress, consider adding version numbers and a changelog. This helps users understand the evolution of the project.
4. **License**: If you want to share this project with certain permissions or restrictions, specify the license under which the project is released (e.g., MIT, GPL, etc.).
5.  **Contact**: Add a section where users can reach out for more detailed queries or potential collaboration.
