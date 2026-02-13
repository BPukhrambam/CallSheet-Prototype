import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'

function App() {
  return (
    <>
      <Navbar />
      <FilmCard />
      <Projects />
    </>
  )
  /* const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  ) */
}

function Navbar() {
  return (
    <div className='navbar-wrapper'>
      <div className='site-title'>
        Callsheet title
      </div>
      <div className='search-bar'>
        <div className='search-selector'>
          Choose projects/people
          <div className='dropdown-icon icon'>

          </div>
        </div>
        <div className='search-field'>
          Search for projects/people
        </div>
        <div className='search-icon icon'>
          Search icon
        </div>
      </div>
      <div className='theme-icon icon'>
          Theme icon
      </div>
      <div className='account-icon icon'>
          Account icon
      </div>
    </div>
  )
}

function FilmCard() {
  return (
    <div className='film-card-wrapper'>
      <h4 className='film-title'>
        Film Title
      </h4>
      <h5 className='film-dates'>
        Film Dates
      </h5>
      <p className='film-details'>
        Logline
      </p>
      <p className='film-details'>
        Roles
      </p>
    </div>
  )
}

function Projects() {
  return (
    <div className='projects-wrapper'>
      <div className='projects-header'>
        <h2>
          EITHER: "Your Projects" or "Find Projects" or "Search Results"
        </h2>
        <div className='projects-header-icon icon'>
          ICON or ICONS, Right Aligned
        </div>
      </div>
      <div className='projects'>
        <FilmCard /> Repeated
      </div>
    </div>
  )
}

export default App
