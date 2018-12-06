# CS-411-Project

Events-APP (primary idea)

The purpose of this app is to never miss out on an amazing events in your area. This app will also use a Facebook authentication service. The app will use your preferences and likes as a filter for events that might interest you. In addition to the Facebook API, it will also make use of the Eventful API which allow you to find events near you. This app will recommend events near you and also will have the option of filtering events ex: by price, location, category. It will utilize a database to store your own profile and the events you like or have gone to, to help recomemnd events that you will like. The goal for this project is to never miss out an opportunity to have some fun. 


Gift-Giver-APP (secondary idea)

The purpose of this app is to try to solve the impossible problem of trying to find a gift for your friends. This App will use a Facebook authentication service, allowing you to log in through your facebook. Once in the app, you can enter in any friends name. The application will search through the friends likes on Facebook, and or some other interests on instagram using the Instagram and Facebook public API's. After find some of your friends interests, you will be recommended products on amazon that corelate to those interests. The amazon products can be sorted and filtered using the Amazon Product Advertising API. Once gifts are found for a friend, say Alex, the gift options presented for Alex will be queried into a database associated with Alex, so that if you would like to find more gifts for Alex in the future, you can just access the options in the database associated with Alex. The goal for this project is to essentially make it easier to find gifts for your family and friends. 


Gift-Giver Functionality explained:

The Gift Giver application first requires the User to use Spotify oAuth to view anything ont the website.
Then on the homepage there are 2 search bars:
  
  1)
  The first search bar you can enter in an ebay item, and a results page will generate with the top 100 matches, you will have   the option to sort by best match, or price ascending/descending. This utilizes the Ebay API.
  
  2)
  The second search bar you can enter in a song name, and an API call will be made to the Spotify API. Then an artist will be   chosen at random from the response of the Spotify API, and an ebay search using the Ebay API will be made for this chosen     artist's merchandise. The results of the Ebay API call can be sorted by best match, or by price ascending/descending.
  
After the results page is generated, you may add any gift you like to your wishlist. This gift will be added to a MYSQL database, and it will correspond to your unique user_id as given by spotify. WHen you add a gift, you will be sent to your wishlist page, with a table that has data on any gift that you have put on your wishlist. You can remove gift entries as you wish.

Lastly, our program utilizes a cache, by saving the most recent spotify track search you have made. If your search value is found in the cache, an API call is avoided, and an artist is chosen at random from the artist list provided in the cache. 

