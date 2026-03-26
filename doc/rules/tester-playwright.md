# Principles for Maintainable Playwright Tests

## 1. Use the Page Object Model (POM)

```typescript
// Example: pages/LoginPage.ts
export class LoginPage {
	private page: Page;

	constructor(page: Page) {
		this.page = page;
	}

	async login(username: string, password: string) {
		await this.page.fill('[data-testid="username"]', username);
		await this.page.fill('[data-testid="password"]', password);
		await this.page.click('[data-testid="login-button"]');
	}
}
```

## 2. Prefer Data-Testid Selectors

```typescript
// Prefer this:
await page.click('[data-testid="submit-button"]');

// Over this:
await page.click('.submit-btn'); // CSS classes may change
await page.click('button:has-text("Submit")'); // Text may change
```

## 3. Create Reusable Test Fixtures

```typescript
// fixtures.ts
export const test = baseTest.extend({
	loggedInPage: async ({ page }, use) => {
		await page.goto('/login');
		await page.fill('[data-testid="username"]', 'testuser');
		await page.fill('[data-testid="password"]', 'password');
		await page.click('[data-testid="login-button"]');
		await use(page);
	}
});
```

## 4. Implement Strong Typing

```typescript
// types.ts
export interface UserData {
	username: string;
	password: string;
	role: 'admin' | 'user' | 'guest';
}

// Using the type in page objects
import { UserData } from '../types';

export class LoginPage {
	private page: Page;

	constructor(page: Page) {
		this.page = page;
	}

	async login(userData: UserData) {
		await this.page.fill('[data-testid="username"]', userData.username);
		await this.page.fill('[data-testid="password"]', userData.password);
		await this.page.click('[data-testid="login-button"]');
	}
}
```

## 5. Isolate Test Data

```typescript
// testData/users.ts
export const testUsers = {
	admin: { username: 'admin1', password: 'securePass1', role: 'admin' },
	regularUser: { username: 'user1', password: 'userPass1', role: 'user' }
};

// In your test:
import { testUsers } from '../testData/users';
test('admin can access settings', async ({ page }) => {
	await loginPage.login(testUsers.admin.username, testUsers.admin.password);
	// Test continues...
});
```

## 6. Implement Robust Wait Strategies

```typescript
// Instead of:
await page.click('[data-testid="submit"]');
await page.waitForTimeout(2000); // Arbitrary delay = flaky tests

// Prefer:
await page.click('[data-testid="submit"]');
await page.waitForSelector('[data-testid="success-message"]');
// Or even better:
await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
```

## 7.

User-facing first: Use roles and accessible names
Semantic meaning: Test IDs should describe purpose, not implementation
Environment agnostic: Work across dev/staging/prod
Data independent: Don't rely on database IDs
Maintainable: Changes to one project don't break other tests

```
// 1. Primary: Role + accessible name (most user-like)
await page.getByRole('button', { name: /work projects/i }).click();

// 2. Secondary: Semantic test ID (stable, meaningful)
await page.getByTestId('project-header-work').click();

// 3. Fallback: CSS selector with semantic class
await page.locator('.project-header[data-project-type="work"]').click();

// 4. Never: Numerical IDs or brittle selectors
// ❌ await page.getByTestId('project-header-2').click();
// ❌ await page.locator('button:nth-child(2)').click();
```

## 12. Use API Calls for Test Setup When Possible

```typescript
test('editing user profile', async ({ page, request }) => {
	// Setup via API instead of UI steps
	const authToken = await getAuthToken(request);
	await request.post('/api/users', {
		headers: { Authorization: `Bearer ${authToken}` },
		data: { name: 'Test User', email: 'test@example.com' }
	});

	// Now test just the UI part you're interested in
	await page.goto('/profile');
	// Continue test...
});
```

## 17. Tag Tests for Better Organization

```typescript
test('basic user can view products @smoke @regression', async ({ page }) => {
	// Test implementation
});

test('admin can manage inventory @admin @regression', async ({ page }) => {
	// Test implementation
});

// Run with: npx playwright test --grep "@smoke"
```

## 18. Create Custom Matchers for Domain Logic

```typescript
// Custom matchers make tests more readable and maintainable
export const todoMatchers = {
	async toBeCompletedTask(locator: Locator) {
		const checkbox = locator.locator('input[type="checkbox"]');
		const isChecked = await checkbox.isChecked();
		const titleElement = locator.locator('[data-testid="task-title"]');
		const hasStrikethrough = await titleElement.evaluate((el) =>
			getComputedStyle(el).textDecoration.includes('line-through')
		);

		return {
			pass: isChecked && hasStrikethrough,
			message: () => `Expected task to be completed (checked and strikethrough)`
		};
	}
};

expect.extend(todoMatchers);

// Usage in tests - more readable than generic assertions
await expect(task).toBeCompletedTask();

// Instead of:
expect(await task.locator('input').isChecked()).toBe(true);
expect(
	await task
		.locator('[data-testid="task-title"]')
		.evaluate((el) => getComputedStyle(el).textDecoration.includes('line-through'))
).toBe(true);
```

## 19. Avoid Nested Interactive Elements and Use Proper ARIA Roles

HTML doesn't allow nested interactive elements like buttons inside buttons. Use semantic structure with proper ARIA roles instead.

```typescript
// ❌ Nested buttons cause HTML validation errors
<button class="task-row">
  <span>Task title</span>
  <button>Menu</button> // Invalid nesting
</button>

// ✅ Use div with interactive role
<div
  role="button"
  tabindex="0"
  onkeydown={handleKeydown}
  onclick={handleClick}
  aria-label="Task: Buy groceries"
>
  <span>Task title</span>
  <button>Menu</button> // Valid - button inside div
</div>

// ✅ Or use proper semantic structure
<li>
  <div
    role="button"
    tabindex="0"
    aria-label="Task: Buy groceries"
  >
    <span>Task title</span>
    <button aria-label="Open menu">⋮</button>
  </div>
</li>
```

**Key Rules:**

- Interactive roles (`button`, `link`, `menuitem`) allow `tabindex` and event listeners
- Semantic roles (`listitem`, `heading`) don't allow interactive behavior
- Use `role="button"` on divs that need click/keyboard interaction
- Always include `aria-label` for screen readers
- Test with keyboard navigation (`Tab`, `Enter`, `Space`)
