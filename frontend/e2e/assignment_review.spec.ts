import { test, expect } from '@playwright/test';

test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== testInfo.expectedStatus) {
    // Get a unique name for the screenshot.
    const screenshotPath = testInfo.outputPath('failure.png');
    // Take the screenshot.
    await page.screenshot({ path: screenshotPath });
    // Attach the screenshot to the report.
    testInfo.attachments.push({ name: 'failure-screenshot', path: screenshotPath, contentType: 'image/png' });
  }
});

test('Assignment Review Page displays problem text and AI analysis', async ({ page }) => {
  // Log console messages
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));

  try {
    await page.goto('http://localhost:3000/'); // Frontend is running on 3000

    // Wait for the content to load. Adjust selector if needed.
    await page.waitForSelector('h1:has-text("Review Submission")', { timeout: 10000 }); // Reduced timeout
    await page.waitForSelector('h3:has-text("Student\'s Problem")');
    await page.waitForSelector('h3:has-text("AI\'s Logical Path")');

    // Check if the hardcoded submission ID's problem text is visible
    const problemTextElement = page.locator('div.bg-white p').first();
    await expect(problemTextElement).toBeVisible();

    // Take a screenshot on success
    await page.screenshot({ path: 'assignment_review_page_success.png', fullPage: true });
    console.log('Screenshot taken: assignment_review_page_success.png');

  } catch (error) {
    await page.screenshot({ path: 'assignment_review_page_error.png', fullPage: true });
    console.log('Error screenshot taken: assignment_review_page_error.png');
    throw error;
  }
});
