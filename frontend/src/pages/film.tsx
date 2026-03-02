import { useParams } from "react-router-dom";
import { dummyData } from '../dummy-data.tsx';

export default function Film() {
  const { FILMID } = useParams();
  const film = dummyData.find(data => data.ID === FILMID);

  if (!film) {
    return <div>Film not found.</div>;
  }
  
  return (
    <>
      <div className="film-page-wrapper">
        <h2 className='film-title'>
          {film.NAME}
        </h2>
        <h5 className='film-dates'>
          {film.DATES}
        </h5>
        <p className='film-details'>
          {film.DESCRIPTION}
        </p>
        <p className='film-details'>
          Roles
        </p>
      </div>
    </>
  );
}

// Add: Contact, Tags