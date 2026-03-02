import { FilmCard } from '../App.tsx'
import { dummyData } from '../dummy-data.tsx';

export default function Results() {
  return (
    <>
    <div className='search-results-wrapper'>
      <h1>Search Results</h1>
      <div className='projects'>
                {dummyData.map((data, key) => ( // REPLACE WITH QUERIED DATA
                  <FilmCard
                    key={key}
                    FILMID={data.ID}
                    NAME={data.NAME}
                    DATES={data.DATES}
                    DESCRIPTION={data.DESCRIPTION}
                  />
                ))}
              </div>
    </div>
    </>
    
  );
}