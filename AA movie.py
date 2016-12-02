import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>My Audiobook List!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("normal", function showNext() {
            $(this).next("div").show("normal", showNext);
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">My Audiobook List</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h2>{movie_title}</h2>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
    
    
    
import webbrowser

class AudioBook():
    """ This Class Provides a way to store AudioBook related information"""
    VALID_RATINGS = ["G","PG","PG-13","R","XXX"]
    def __init__(self, title, storyline, poster_image_url,trailer_youtube_url):
        self.title = title
        self.storyline = storyline
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url
    
    def show_trailer(self):
        """plays the movie trailer"""
        webbrowser.open(self.trailer_youtube_url)
        






Elon_Musk = AudioBook("Elon Musk", 
                            "Tesla, SpaceX, and the Quest for a Fantastic Future",
                            "https://upload.wikimedia.org/wikipedia/en/a/a8/Elon_Musk_-_Tesla%2C_SpaceX%2C_and_the_Quest_for_a_Fantastic_Future.jpg",
                            "https://www.youtube.com/watch?v=xsKtsPYCPeQ"
                            )

The_Innovators = AudioBook("The Innovators",
                                 "How a Group of Inventors, Hackers, Geniuses, and Geeks Created the Digital Revolution",
                                 "http://t0.gstatic.com/images?q=tbn:ANd9GcQ63yJkdn3-hjloY2XJLJAKvHlTC-g1GBWz3rWs7d7lj1inRpnI",
                                 "http://www.audible.com/pd/Science-Technology/The-Innovators-Audiobook/B00M9KA2ZM/ref=a_search_c4_1_1_srImg?qid=1479364117&sr=1-1"
                                 )

Steve_Jobs = AudioBook("Steve Jobs By Walter Isaacson",
                             "Steve Jobs is the authorized self-titled biography book of Steve Jobs. The book was written at the request of Jobs by Walter Isaacson, a former executive at CNN and TIME who has written best-selling biographies of Benjamin Franklin and Albert Einstein.[1][2]",
                             "https://upload.wikimedia.org/wikipedia/en/e/e4/Steve_Jobs_by_Walter_Isaacson.jpg",
                             "https://www.youtube.com/watch?v=sGvrPjB68uw"
                             )

ISIS_Inside = AudioBook("ISIS: Inside the Army of Terror",
                              "ISIS: Inside the Army of Terror is a 2015 non-fiction book by the journalists Michael Weiss and Hassan Hassan. The book details the rise and inner workings of the terrorist group ISIS.[1]",
                              "https://images-na.ssl-images-amazon.com/images/I/414fH9JvMwL._SX328_BO1,204,203,200_.jpg", 
                              "https://www.youtube.com/watch?v=4MbRvqr34UM")


Dale_Carnegie = AudioBook("How to Win Friends and Influence People",
                                "How to Win Friends and Influence People is one of the first best-selling self-help books ever published. Written by Dale Carnegie (1888-1955) and first published in 1936, it has sold over 30 million copies world-wide, and went on to be named #19 on Time Magazine's list of 100 most influential books in 2011.[1]",
                                "https://upload.wikimedia.org/wikipedia/en/3/33/How-to-win-friends-and-influence-people.jpg",
                                "https://www.youtube.com/watch?v=YcNfyBJILZE"
                                )   

Presuasion = AudioBook("Pre-Suasion: A Revolutionary Way to Influence and Persuade",
                             "The great social psychologist Robert Cialdini has written another timeless and indispensable book about the psychology of influence. I'll be recommending it for years and years.",
                             "http://www.socialmediaexaminer.com/wp-content/uploads/2016/09/ms-pre-suasion.png",
                             "https://www.youtube.com/watch?v=ZzLup7EQQM8"
                             )   

Delivering_Happiness = AudioBook("Delivering Happiness: A Path to Profits, Passion, and Purpose by Tony Hsieh",
                                       "You want to learn about the path that we took at Zappos to get to over $1 billion in gross merchandise sales in less than ten years.",
                                       "https://images-na.ssl-images-amazon.com/images/I/51OqvVJykPL._SX258_BO1,204,203,200_.jpg",
                                       "http://www.goodreads.com/book/show/6828896-delivering-happiness"
                                       )   

Membership_economy = AudioBook("Pre-Suasion: A Revolutionary Way to Influence and Persuade",
                                     "The great social psychologist Robert Cialdini has written another timeless and indispensable book about the psychology of influence. I'll be recommending it for years and years.",
                                     "https://smallbiztrends.com/wp-content/uploads/2015/01/the-membership-economy.jpg",
                                     "http://www.goodreads.com/book/show/22573915-the-membership-economy"
                                     )   


How_Google_Works = AudioBook("How Google Works",
                                   "Both Eric Schmidt and Jonathan Rosenberg came to Google as seasoned Silicon Valley business executives...",
                                   "https://images-na.ssl-images-amazon.com/images/I/617VQLnBcVL.jpg",
                                   "http://www.goodreads.com/book/show/23158207-how-google-works"
                                   )   





AudioBooks = [Elon_Musk,The_Innovators, Steve_Jobs, ISIS_Inside, Dale_Carnegie, Presuasion, Delivering_Happiness, Membership_economy, How_Google_Works]
open_movies_page(AudioBooks)






