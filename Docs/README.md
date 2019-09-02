# CS-411-Project

Gift-Giver Functionality explained:

The Gift Giver application first requires the User to use Spotify oAuth to view anything ont the website.
Then on the homepage there are 2 search bars:
  
  1)
  The first search bar you can enter in an ebay item, and a results page will generate with the top 100 matches, you will have   the option to sort by best match, or price ascending/descending. This utilizes the Ebay API.
  
  2)
  The second search bar you can enter in a song name, and an API call will be made to the Spotify API. Then an artist will be   chosen at random from the response of the Spotify API, and an ebay search using the Ebay API will be made for this chosen     artist's merchandise. The results of the Ebay API call can be sorted by best match, or by price ascending/descending.
  
After the results page is generated, you may add any gift you like to your wishlist. This gift will be added to a MYSQL database, and it will correspond to your unique user_id as given by spotify. WHen you add a gift, you will be sent to your wishlist page, with a table that has data on any gift that you have put on your wishlist. You can remove gift entries as you wish.

Lastly, our program utilizes a cache, by saving the most recent spotify track search you have made. If your search value is found in the cache, an API call is avoided, and an artist is chosen at random from the artist list provided in the cache. 


--NOTE:
  All content in static folder was not written by me and has been credited to the proper sources. All the folder contains is     css templates that provide the website style.
