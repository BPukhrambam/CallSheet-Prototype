const apiURL = "";

export function fetchData(request: String) {
  fetch(apiURL + request)
  .then(response => {
    if (response.ok) {
      return response.json();
    }
    else {
      throw new Error('API request failed')
    }
  })
}


/*export const data: {
  ID: string;
  NAME: string;
  DATES: string;
  DESCRIPTION: string;
  USER_ID: string;
}[] = fetchData(request);*/

export const dummyData: {
  ID: string;
  NAME: string;
  DATES: string;
  DESCRIPTION: string;
  USER_ID: string;
}[] = [
  {
    "ID": "1",
    "NAME": "MANEATER",
    "DATES": "11/10/23",
    "DESCRIPTION": "SUCH A GOOD FILM",
    "USER_ID": "1"
  },
  {
    "ID": "2",
    "NAME": "HARMONY OF HEARTS",
    "DATES": "12/2/23",
    "DESCRIPTION": "SUCH A GOOD FILM",
    "USER_ID": "1"
  },
  {
    "ID": "3",
    "NAME": "TRUTH SEEKER",
    "DATES": "8/10/23",
    "DESCRIPTION": "SUCH A GOOD FILM",
    "USER_ID": "1"
  },
  {
    "ID": "4",
    "NAME": "STARLIGHT DREAMS",
    "DATES": "7/15/23",
    "DESCRIPTION": "A CAPTIVATING ROMANCE",
    "USER_ID": "1"
  },
  {
    "ID": "5",
    "NAME": "MYSTERIOUS SHADOWS",
    "DATES": "6/5/23",
    "DESCRIPTION": "A THRILLING MYSTERY",
    "USER_ID": "1"
  },
  {
    "ID": "6",
    "NAME": "SUNSET SERENADE",
    "DATES": "9/20/23",
    "DESCRIPTION": "A HEARTWARMING MUSICAL",
    "USER_ID": "1"
  },
  {
    "ID": "7",
    "NAME": "ETERNAL ECLIPSE",
    "DATES": "4/1/23",
    "DESCRIPTION": "A DARK FANTASY EPIC",
    "USER_ID": "1"
  },
  {
    "ID": "8",
    "NAME": "LOST IN TIME",
    "DATES": "2/12/23",
    "DESCRIPTION": "A TIME-TRAVEL ADVENTURE",
    "USER_ID": "1"
  },
  {
    "ID": "9",
    "NAME": "ENCHANTED GARDEN",
    "DATES": "10/8/23",
    "DESCRIPTION": "A MAGICAL FAMILY FILM",
    "USER_ID": "1"
  },
  {
    "ID": "10",
    "NAME": "UNCHARTED WATERS",
    "DATES": "3/25/23",
    "DESCRIPTION": "A HIGH-SEAS ADVENTURE",
    "USER_ID": "1"
  },
  {
    "ID": "11",
    "NAME": "BEYOND THE STARS",
    "DATES": "5/30/23",
    "DESCRIPTION": "AN INTERGALACTIC JOURNEY",
    "USER_ID": "1"
  },
  {
    "ID": "12",
    "NAME": "WHISPERS IN THE WOODS",
    "DATES": "11/18/23",
    "DESCRIPTION": "A HAUNTING HORROR",
    "USER_ID": "1"
  },
  {
    "ID": "13",
    "NAME": "CELESTIAL HARMONY",
    "DATES": "7/5/23",
    "DESCRIPTION": "A SCI-FI ODYSSEY",
    "USER_ID": "1"
  },
  {
    "ID": "14",
    "NAME": "SERENADE UNDER THE MOON",
    "DATES": "1/9/23",
    "DESCRIPTION": "A ROMANTIC COMEDY",
    "USER_ID": "1"
  },
  {
    "ID": "15",
    "NAME": "THE LOST KINGDOM",
    "DATES": "8/27/23",
    "DESCRIPTION": "AN EPIC FANTASY QUEST",
    "USER_ID": "1"
  },
  {
    "ID": "16",
    "NAME": "CITY OF ILLUSIONS",
    "DATES": "6/18/23",
    "DESCRIPTION": "A PSYCHOLOGICAL THRILLER",
    "USER_ID": "1"
  },
  {
    "ID": "17",
    "NAME": "CHASING DREAMS",
    "DATES": "9/12/23",
    "DESCRIPTION": "A DRAMA OF AMBITIONS",
    "USER_ID": "1"
  },
  {
    "ID": "18",
    "NAME": "SECRET OF THE ORACLE",
    "DATES": "4/28/23",
    "DESCRIPTION": "A MYSTICAL ADVENTURE",
    "USER_ID": "1"
  },
  {
    "ID": "19",
    "NAME": "STARDUST MEMORIES",
    "DATES": "2/5/23",
    "DESCRIPTION": "A NOSTALGIC JOURNEY",
    "USER_ID": "1"
  },
  {
    "ID": "20",
    "NAME": "UNDERGROUND REBELLION",
    "DATES": "10/15/23",
    "DESCRIPTION": "A DYSTOPIAN ACTION",
    "USER_ID": "1"
  },
  {
    "ID": "21",
    "NAME": "WHEN SHADOWS FALL",
    "DATES": "5/8/23",
    "DESCRIPTION": "A SUPERNATURAL MYSTERY",
    "USER_ID": "1"
  },
  {
    "ID": "22",
    "NAME": "LOVE IN BLOOM",
    "DATES": "12/7/23",
    "DESCRIPTION": "A ROMANTIC DRAMA",
    "USER_ID": "1"
  },
  {
    "ID": "23",
    "NAME": "THE TIMELESS VOYAGE",
    "DATES": "8/3/23",
    "DESCRIPTION": "A TIME-TRAVEL ROMANCE",
    "USER_ID": "1"
  }
]