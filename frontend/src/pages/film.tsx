import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchData, type ProjectData } from '../data.tsx';

export default function Film() {
  const { FILMID } = useParams();
  const [film, setFilm] = useState<ProjectData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFilm = async () => {
      if (!FILMID) {
        setLoading(false);
        return;
      }

      try {
        const projects = await fetchData();
        const selectedFilm = projects.find((data) => data.ID === FILMID) ?? null;
        setFilm(selectedFilm);
      } finally {
        setLoading(false);
      }
    };

    loadFilm();
  }, [FILMID]);

  if (loading) {
    return <div>Loading...</div>;
  }

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