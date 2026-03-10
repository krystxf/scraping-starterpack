const fs = require("fs");
const path = require("path");
const FormData = require("form-data");
const fetch = require("node-fetch");

const API_URL = "http://localhost:3100/extract-text";
const DATA_DIR = path.join(__dirname, "data");

// Normalize text for comparison (remove spaces, convert to lowercase)
function normalizeText(text) {
  return text.replace(/\s+/g, "").toLowerCase().trim();
}

// Extract expected text from filename (remove extension)
function getExpectedText(filename) {
  return path.basename(filename, path.extname(filename));
}

// Test a single image file
async function testImage(filePath) {
  const filename = path.basename(filePath);
  const expectedText = getExpectedText(filename);
  const startTime = Date.now();

  try {
    // Create form data with image file
    const form = new FormData();
    form.append("image", fs.createReadStream(filePath));

    // Send request to API
    const response = await fetch(API_URL, {
      method: "POST",
      body: form,
      headers: form.getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || "Unknown error");
    }

    const extractedText = normalizeText(result.text);
    const expectedNormalized = normalizeText(expectedText);

    const isCorrect = extractedText === expectedNormalized;
    const duration = Date.now() - startTime;

    return {
      filename,
      expected: expectedText,
      extracted: result.text,
      normalizedExtracted: extractedText,
      normalizedExpected: expectedNormalized,
      correct: isCorrect,
      duration,
    };
  } catch (error) {
    const duration = Date.now() - startTime;
    console.error(`Error testing ${filename}:`, error.message);
    return {
      filename,
      expected: expectedText,
      extracted: null,
      normalizedExtracted: null,
      normalizedExpected: normalizeText(expectedText),
      correct: false,
      error: error.message,
      duration,
    };
  }
}

// Check if API is available
async function checkAPI() {
  try {
    const response = await fetch("http://localhost:3100/health");
    if (response.ok) {
      const health = await response.json();
      console.log(
        `API is running (Model: ${health.model}, Device: ${health.device})\n`,
      );
      return true;
    }
  } catch (error) {
    console.error(`\nError: Cannot connect to API at ${API_URL}`);
    console.error("Make sure the backend server is running on port 3100\n");
    return false;
  }
  return false;
}

// Main function
async function main() {
  console.log("Starting accuracy test...\n");
  console.log(`API URL: ${API_URL}`);
  console.log(`Data directory: ${DATA_DIR}\n`);

  // Check if API is available
  const apiAvailable = await checkAPI();
  if (!apiAvailable) {
    process.exit(1);
  }

  // Read all files from data directory
  const files = fs
    .readdirSync(DATA_DIR)
    .filter((file) => {
      const ext = path.extname(file).toLowerCase();
      return ext === ".png" || ext === ".jpg" || ext === ".jpeg";
    })
    .map((file) => path.join(DATA_DIR, file));

  console.log(`Found ${files.length} image files to test\n`);

  if (files.length === 0) {
    console.log("No image files found in data directory!");
    return;
  }

  const results = [];
  let processed = 0;
  let correctCount = 0;

  // Test each file
  for (const file of files) {
    processed++;
    const result = await testImage(file);
    results.push(result);

    // Update correct count
    if (result.correct) {
      correctCount++;
    }

    // Calculate current accuracy
    const currentAccuracy = (correctCount / processed) * 100;

    // Calculate current average speed
    const totalDuration = results.reduce(
      (sum, r) => sum + (r.duration || 0),
      0,
    );
    const averageDuration = totalDuration / processed;
    const requestsPerSecond = (1000 / averageDuration).toFixed(2);

    // Show progress with real-time accuracy and average speed
    const status = result.correct ? "✓" : "✗";
    process.stdout.write(
      `\r[${processed}/${files.length}] ${status} ${
        result.filename
      } | Accuracy: ${currentAccuracy.toFixed(
        2,
      )}% (${correctCount}/${processed}) | Avg Speed: ${averageDuration.toFixed(
        2,
      )}ms (${requestsPerSecond} req/s)`,
    );

    // Small delay to avoid overwhelming the API
    await new Promise((resolve) => setTimeout(resolve, 100));
  }

  console.log("\n\n" + "=".repeat(80));
  console.log("RESULTS");
  console.log("=".repeat(80));

  // Calculate statistics
  const correct = results.filter((r) => r.correct).length;
  const incorrect = results.filter((r) => !r.correct).length;
  const accuracy = (correct / results.length) * 100;

  // Calculate speed statistics
  const durations = results.map((r) => r.duration || 0).filter((d) => d > 0);
  const totalDuration = durations.reduce((sum, d) => sum + d, 0);
  const averageDuration = totalDuration / durations.length;
  const minDuration = Math.min(...durations);
  const maxDuration = Math.max(...durations);
  const requestsPerSecond = (1000 / averageDuration).toFixed(2);

  console.log(`\nTotal files tested: ${results.length}`);
  console.log(`Correct: ${correct}`);
  console.log(`Incorrect: ${incorrect}`);
  console.log(`\nAccuracy: ${accuracy.toFixed(2)}%`);
  console.log(`\nSpeed Statistics:`);
  console.log(
    `  Average: ${averageDuration.toFixed(2)}ms (${requestsPerSecond} req/s)`,
  );
  console.log(`  Min: ${minDuration.toFixed(2)}ms`);
  console.log(`  Max: ${maxDuration.toFixed(2)}ms`);
  console.log(`  Total time: ${(totalDuration / 1000).toFixed(2)}s\n`);

  // Show incorrect results
  const incorrectResults = results.filter((r) => !r.correct);
  if (incorrectResults.length > 0) {
    console.log("Incorrect results:");
    console.log("-".repeat(80));
    incorrectResults.slice(0, 20).forEach((result) => {
      console.log(`\nFile: ${result.filename}`);
      console.log(`  Expected: "${result.expected}"`);
      console.log(`  Extracted: "${result.extracted || "ERROR"}"`);
      if (result.error) {
        console.log(`  Error: ${result.error}`);
      }
    });

    if (incorrectResults.length > 20) {
      console.log(
        `\n... and ${incorrectResults.length - 20} more incorrect results`,
      );
    }
  }

  console.log("\n" + "=".repeat(80));
}

// Run the test
main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
