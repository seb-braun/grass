const { test, expect } = require("@playwright/test");

const plantAssets = {
  "plant.svg": "A leafy green plant in a terracotta pot",
  "cactus.svg": "A green cactus in a terracotta pot",
  "sunflower.svg": "A yellow sunflower in a terracotta pot",
  "succulent.svg": "A rosette succulent in a terracotta pot",
};

test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

test("starts with an empty garden and zero plants", async ({ page }) => {
  const garden = page.getByRole("group", { name: "Your garden" });

  await expect(page.locator("#count")).toHaveText("0");
  await expect(garden.locator("img")).toHaveCount(0);
  await expect
    .poll(() => garden.evaluate((element) => getComputedStyle(element, "::before").content))
    .toContain("Your garden is empty");
});

test("planting adds one loaded, described bundled image per click", async ({ page }) => {
  const garden = page.getByRole("group", { name: "Your garden" });
  const plantButton = page.getByRole("button", { name: "Plant a seedling" });

  for (const count of [1, 2, 3]) {
    await plantButton.click();
    await expect(garden.locator("img")).toHaveCount(count);
    await expect(page.locator("#count")).toHaveText(String(count));
  }

  for (const image of await garden.locator("img").all()) {
    const source = await image.getAttribute("src");
    expect(Object.keys(plantAssets)).toContain(source);
    await expect(image).toHaveAttribute("alt", plantAssets[source]);
    await expect
      .poll(() => image.evaluate((element) => element.complete && element.naturalWidth > 0))
      .toBe(true);

    const response = await page.request.get(new URL(source, page.url()).href);
    expect(response.ok()).toBe(true);
    expect(response.headers()["content-type"]).toContain("image/svg+xml");
  }
});

test("reset clears the garden and planting remains usable", async ({ page }) => {
  const garden = page.getByRole("group", { name: "Your garden" });
  const plantButton = page.getByRole("button", { name: "Plant a seedling" });

  await plantButton.click();
  await plantButton.click();
  await expect(garden.locator("img")).toHaveCount(2);

  await page.getByRole("button", { name: "Reset" }).click();
  await expect(garden.locator("img")).toHaveCount(0);
  await expect(page.locator("#count")).toHaveText("0");

  await plantButton.click();
  await expect(garden.locator("img")).toHaveCount(1);
  await expect(page.locator("#count")).toHaveText("1");
});

test("plant and reset actions are keyboard reachable and activatable", async ({ page }) => {
  await page.keyboard.press("Tab");
  await expect(page.locator("#plant")).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.locator("#count")).toHaveText("1");

  await page.keyboard.press("Tab");
  await expect(page.locator("#reset")).toBeFocused();
  await page.keyboard.press("Space");
  await expect(page.locator("#count")).toHaveText("0");
});
