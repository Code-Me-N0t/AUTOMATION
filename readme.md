<h1>iGAMING FUNCTIONAL TESTING AUTOMATION</h1>
<p>This pytest automation script is designed to test various functionalities of a gaming web application.</p>
<span>Below is a brief overview of the script files and their functionalities:</span>

<h2>TESTS</h2>
<ul>
  <li>Conftest: This file handles the webdriver configuration including some test fixtures for test script customization.</li>
  <li>Test Multi: This file contains all the test scenario for the Multi feature. It covers the core functions scenario. It includes a variety of game options for the available games displayed in Multi</li>
  <li>Test Sidebet: This file contains all the test scenario for the Sidebet Feature. It covers the core functions scenario. It includes a variety of game options for the available games displayed in Sidebet</li>
</ul>

<h2>SRC</h2>
<ul>
  <li>Modules: This file contains al the non-driver pre-requisite methods needed to run the script.</li>
  <li>Multi Main: This files containes the main test logic of the Multi feature. This include as well the test cases created for the mentioned feature.</li>
  <li>Sidebet Main: This files containes the main test logic of the Sidebet feature. This include as well the test cases created for the mentioned feature.</li>
</ul>

<h2>HANDLERS</h2>
<ul>
  <li>API Handler: Contains the API methods for multiple functions including generating the token and game URL</li>
  <li>Element Handler: Contains set of methods to interact with web elements directly. It simplifies common actions such as finding elements, clicking elements, and waiting for conditions that directly involves the element</li>
  <li>Task Handler: Contains set of methods for handling a variety of tasks specific to the game itself, includes navigating and interacting with the user interface.</li>
</ul>

<h2>RESOURCES</h2>
<ul>
  <li>Credentials: Contains credentials for the Google Sheet report.</li>
  <li>Creds: A json file that contains sensitive game informations such as base url, token name, etc.</li>
  <li>Locator: A yaml file for storing element selectors for locating web elements.</li>
  <li>Scenarios: A json file for storing test scenarios.</li>
  <li>Script: A javascript file that contains javscript methods for specific functions.</li>
  <li>Token: A json file for enabling google API</li>
</ul>

<h2>TERMINAL COMMANDS</h2>
<p>Below are the commands for running the script</p>
<ul>
  <li>"pytest": To recognize the script as a Pytest script. (required)</li>
  <li>"-s": To display print outputs.</li>
  <li>"-v": To increase the verbosity of the log outputs.</li>
  <li>"-m": To run test with specific markers. Markers are available in running Sidebet script ("single"/"multiple")</li>
  <li>Game Options: Specifies the game to test. Refer to the test files to see the available games listed. You may run the code using (e.g., "--DT")</li>
</ul>

<i>Note: To run the script you need to have your creds.json for handling game credentials, as well as credentials.json for generating google sheet report</i><br>
<i>Note: This readme provides a high-level overview of the pytest automation script. For detailed implementation and usage instructions, refer to the comments within the script files (test and main) and the corresponding modules (src/modules.py and src/helpers.py).</i>
