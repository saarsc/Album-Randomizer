using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Net.Http;
using System.Net;
using HtmlAgilityPack;
using System.Data;
using System.Data.SqlClient;
using System.ComponentModel;


namespace Album_Randomizer
{
    /// <summary>
    /// Interaction logic for SelectAlbums.xaml
    /// </summary>
    public partial class SelectAlbums : Window
    {
        private string albumId;
        private string artistName;
        private SearchArtist SearchArtistView;


        public SelectAlbums(string id, string artistName, SearchArtist searchArtistView)
        {
            InitializeComponent();

            this.albumId = id;
            this.artistName = artistName;
            this.SearchArtistView = searchArtistView;
            getAlbumsList();

        }


        private async void getAlbumsList()
        {

            HttpClientHandler handler = new HttpClientHandler
            {
                AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate
            };

            HttpClient httpClient = new HttpClient(handler);
            httpClient.DefaultRequestHeaders.Add("Connection", "close");
            httpClient.DefaultRequestHeaders.Add("Accept", "text/html, */*; q=0.01");
            httpClient.DefaultRequestHeaders.Add("X-Requested-With", "XMLHttpRequest");
            httpClient.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36");
            httpClient.DefaultRequestHeaders.Add("Origin", "https://www.allmusic.com");
            httpClient.DefaultRequestHeaders.Add("Sec-Fetch-Site", "same-origin");
            httpClient.DefaultRequestHeaders.Add("Sec-Fetch-Mode", "cors");
            httpClient.DefaultRequestHeaders.Add("Sec-Fetch-Dest", "empty");
            httpClient.DefaultRequestHeaders.Add("Referer", "https://www.allmusic.com/advanced-search");
            httpClient.DefaultRequestHeaders.Add("Accept-Encoding", "gzip, deflate");
            httpClient.DefaultRequestHeaders.Add("Accept-Language", "en-US,en;q=0.9");

            FormUrlEncodedContent payload = new FormUrlEncodedContent(new[] {
                //new KeyValuePair <string,string>("filters[]","editorialrating:9|editorialrating:8|editorialrating:7|editorialrating:6|editorialrating:5"),
                new KeyValuePair <string,string>("filters[]","recordingtype:mainalbum"),
                new KeyValuePair <string,string>("filters[]","performerid:" + this.albumId),
                new KeyValuePair <string,string>("sort","")
            });

            var response = await httpClient.PostAsync("https://www.allmusic.com:443/advanced-search/results/", payload);
            var reponseString = await response.Content.ReadAsStringAsync();
            var parser = new HtmlDocument();
            parser.LoadHtml(reponseString);

            var names = parser.DocumentNode.SelectNodes("//tbody/tr/td[4]");

            List<album> albums = new List<album>();
            //ADD CHECK FOR NAMES = NULL -> Display error no albums found
            for (var i = 0; i < names.Count; i++)
            {
                album newAlbum = new album { Name = names[i].InnerText.Trim(), ID = i, IsSelected = true };
                albums.Add(newAlbum);
                //albumsToAddList.Add(newAlbum);
            }

            lbWrapper.ItemsSource = albums;

        }



        private void btnConfirm_Click(object sender, RoutedEventArgs e)
        {
            int rowCount = 0;
            var albumName = "";

            var strConn = "Data Source=(LocalDB)\\MSSQLLocalDB;AttachDbFilename=C:\\Users\\user\\Documents\\Random Scripts\\Album Randomizer\\Album Randomizer\\AlbumDatabase.mdf;Integrated Security=True";
            SqlConnection sql = new SqlConnection(strConn);
            SqlCommand cmd = new SqlCommand();

            cmd.CommandType = CommandType.Text;
            cmd.Connection = sql;
            sql.Open();

            var allCheckboxes = lbWrapper.ItemsSource as IEnumerable<album>;
            foreach (var newAlbum in allCheckboxes)
            {

                albumName = newAlbum.Name;

                cmd.CommandText = "SELECT * FROM Albums WHERE artist = '" + this.artistName + "' and album = '" + albumName + "'";

                var result = cmd.ExecuteScalar();
                if (result != null)
                {
                    continue;
                }
                
                cmd.CommandText = "INSERT INTO Albums (artist,album,useAlbum) VALUES ('" + this.artistName + "', '" + albumName + "' , '" + newAlbum.IsSelected  + "')";
                cmd.ExecuteNonQuery();



            }
            sql.Close();
            SearchArtistView.Show();
            this.Close();
        }
        /*
                private void lbWrapper_SelectionChanged(object sender, SelectionChangedEventArgs e)
                {
                    foreach (album item in e.AddedItems)
                    {
                        albumsToAddList.Add(item);

                    }
                    foreach (album item in e.RemovedItems)
                    {
                        albumsToAddList.Remove(item);

                    }

                }*/

        private void selectAll_Checked(object sender, RoutedEventArgs e)
        {
            UpdateCheckBoxes(true);
        }

        private void selectAll_Unchecked(object sender, RoutedEventArgs e)
        {
            UpdateCheckBoxes(false);
        }

        private void UpdateCheckBoxes(bool state)
        {
            var allCheckboxes = lbWrapper.ItemsSource as IEnumerable<album>;
            foreach (var checkbox in allCheckboxes)
            {
                checkbox.IsSelected = state;
            }

        }

        private class album : INotifyPropertyChanged
        {
            public event PropertyChangedEventHandler PropertyChanged;

            public bool selected { get; set; }
            public int ID { get; set; }
            public string Name { get; set; }
            public bool IsSelected
            {
                get
                {
                    return this.selected;
                }
                set
                {
                    if (value != this.selected)
                    {
                        this.selected = value;
                        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(""));
                    }
                }
            }

        }

    }


}
