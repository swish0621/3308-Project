<b>Webpage Deliverables & Testing</b>

<hr>

<img src="images/homepage.png" alt="homepage screenshot" WIDTH=100% ALIGN="left" style="margin:5px" /> <br>

<img src="images/cod.png" alt="call of duty screenshot" WIDTH=100% ALIGN="left" style="margin:5px" /> <br>

<img src="images/dym_gta.png" alt="did you mean grand theft auto screenshot" WIDTH=100% ALIGN="left" style="margin:5px" /> <br>

<img src="images/gta.png" alt="grand theft auto screenshot" WIDTH=100% ALIGN="left" style="margin:5px" /> <br>

<img src="images/dym_overwatch.png" alt="did you mean overwatch screenshot" WIDTH=100% ALIGN="left" style="margin:5px" /> <br>

<img src="images/overwatch.png" alt="overwatch screenshot" WIDTH=100% ALIGN="left" style="margin:5px" /> <br>

<img src="images/fortnight.png" alt="fortnight screenshot" WIDTH=100% ALIGN="left" style="margin:5px" /> <br>



<hr>

<b>Tests:</b>
    <br>
plain code without markdown formatting can be found in /3308-Project/frontend/sentiment_app/src/App.test.js <br>

<hr>

import React from 'react'; <br>
import { render, screen, fireEvent } from '@testing-library/react'; <br>
import '@testing-library/jest-dom';<br>
import userEvent from '@testing-library/user-event';<br>
import App from './App';<br>


// tests that the page is loadable and contains a title<br>
test('Any: render a page with title', () => {<br>
  render(<App />);<br>

    const headings = screen.getAllByRole('heading');
    const h1 = headings.find(h => h.tagName === 'H2');
    expect(h1).toBeInTheDocument();
});<br>

// tests that the page contains a search bar <br>
test('Any: render search bar', () => {<br>
  render(<App />);<br>

  const searchBar = screen.getByPlaceholderText(/Search games\.\.\./i);<br>
  expect(searchBar).toBeInTheDocument();<br>
});<br>

// test that the home page contains 6 linked tiles<br>
// if we add more links to the home page we can change the expected length <br>
test('Home: page contains 6 tile links', () => {<br>
  render(<App />);<br>

  const links = screen.getAllByRole('link');<br>
  expect(links).toHaveLength(6);<br>
});<br>

// test that links have valid contents<br>
test('Any: check link validity', () => {<br>
  render(<App />);<br>
  
  const links = screen.getAllByRole('link');<br>
  links.forEach(link => {<br>
    const href = link.getAttribute('href');<br>
    expect(href).toBeTruthy();<br>
    // matches "/" for relative path, "http://"" or "https://""<br>
    expect(href).toMatch(/^(\/|https?\/\/)/)<br>
  })<br>
});<br>

//test you can type into the search bar <br>
test('Any: search bar updates', async () => {<br>
  render(<App />);<br>

  const input = screen.getByPlaceholderText(/Search games\.\.\./i);<br>
  await userEvent.type(input, 'testing');<br>
  expect(input).toHaveValue('testing');<br>
});<br>
