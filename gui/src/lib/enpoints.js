// Base URL for the backend server
const BASE_URL = 'http://localhost:5000'; // Replace with your actual server URL

// Define API endpoints
export const ENDPOINTS = {
  getGameData: `${BASE_URL}/api/game/data`,
  makeMove: `${BASE_URL}/api/game/move`,
  AIResponse: `${BASE_URL}/api/game/ai-response`,
  // Add other endpoints as needed
};
