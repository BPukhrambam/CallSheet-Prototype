import { dummyData } from './dummy-data.tsx';
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import accountIcon from './assets/account_circle.svg'
import bookmarkIcon from './assets/Bookmark.svg'
import dropdownIcon from './assets/Chevron down.svg'
import goIcon from './assets/Corner up-right.svg'
import editIcon from './assets/Edit.svg'
import gridIcon from './assets/Grid.svg'
import listIcon from './assets/List.svg'
import moonIcon from './assets/Moon.svg'
import plusIcon from './assets/Plus.svg'
import searchIcon from './assets/Search.svg'
import sunIcon from './assets/Sun.svg'
// import fetchData from './dummy-data.tsx'


import './App.css'

function App() {
  return (
    <>
      <Navbar />
      <div className='side-by-side'>
        <Projects name="Your Projects" icon={plusIcon}/>
        <Projects name="Community Projects" icon={goIcon}/>
      </div>
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
      <div className='navbar-item site-title'>
        Callsheet title
      </div>
      <div className='navbar-item search-bar'>
        <select className='search-selector'>
          <option>Projects</option>
          <option>People</option>
        </select>
        <div className='search-field'>
          Search for projects/people
        </div>
        <img src={searchIcon} className="search-icon icon" alt="Search icon" />
      </div>
      <img src={sunIcon} className="navbar-item theme-icon icon" alt="Theme icon, sun" />
      <img src={accountIcon} className="navbar-item account-icon icon" alt="Account icon" />
    </div>
  )
}
// <img src={dropdownIcon} className="dropdown-icon icon" alt="Dropdown icon" />
/* export const Films = () => {
  return (
    <>
      <div className="film-container">
        {dummyData.map((data, key) => {
          return (
            <div key={key}>
              <FilmCard
                key={key}
                NAME={data.NAME}
                DATES={data.DATES}
                DESCRIPTION={data.DESCRIPTION}
              />
            </div>
          );
        })}
      </div>
    </>
  );
}; */

const FilmCard = ({ NAME, DATES, DESCRIPTION }: { NAME?: string; DATES?: string; DESCRIPTION?: string }) => {
  if (!NAME) return <div />;
  return (
    <div className='film-card-wrapper'>
      <h4 className='film-title'>
        {NAME}
      </h4>
      <h5 className='film-dates'>
        {DATES}
      </h5>
      <p className='film-details'>
        {DESCRIPTION}
      </p>
      <p className='film-details'>
        Roles
      </p>
    </div>
  )
}

function Projects({name, icon}: {name?: string; icon?: string;}) {
  return (
    <div className='projects-wrapper'>
      <div className='projects-header'>
        <h2 className='projects-header-title'>
          {name}
        </h2>
        <img src={icon} className="projects-header-icon icon" alt="Action icon" />
      </div>
      <div className='projects'>
        {dummyData.map((data, key) => ( // REPLACE WITH QUERIED DATA
          <FilmCard
            key={key}
            NAME={data.NAME}
            DATES={data.DATES}
            DESCRIPTION={data.DESCRIPTION}
          />
        ))}
      </div>
    </div>
  )
}

export default App
