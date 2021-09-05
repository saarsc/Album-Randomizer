using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Net.Http;
using System.Net;
using HtmlAgilityPack;

namespace Album_Randomizer
{
    /// <summary>
    /// Interaction logic for SearchArtist.xaml
    /// </summary>
    public partial class SearchArtist : Window
    {
        public string Id { get; private set; }

        public SearchArtist()
        {
            InitializeComponent();

            EditArtists editArtists = new EditArtists();
            editArtists.Show();
        }

        private void btnSearchArtist_Click(object sender, RoutedEventArgs e)
        {
            submitForm();
        }

        private void submitForm()
        {
            string artist = tbSearchArtist.Text;

            searchArtist(artist);
        }

        private async void searchArtist(String artist)
        {
            WebProxy proxy = new WebProxy
            {
                Address = new Uri($"http://127.0.0.1:8080"),
                BypassProxyOnLocal = false
            };

            HttpClientHandler handler = new HttpClientHandler
            {
                AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate
            };

            /*handler.ClientCertificateOptions = ClientCertificateOption.Manual;
            handler.ServerCertificateCustomValidationCallback =
            (httpRequestMessage, cert, cetChain, policyErrors) =>
            {
                return true;
            };*/
            //HttpClient httpClient = new HttpClient(handler: handler, disposeHandler: true);
            HttpClient httpClient = new HttpClient(handler);

            String URL = "https://www.allmusic.com:443/search/typeahead/artist/" + artist;

            httpClient.DefaultRequestHeaders.Add("Connection", "close");
            httpClient.DefaultRequestHeaders.Add("Accept", "*/*");
            httpClient.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36");
            httpClient.DefaultRequestHeaders.Add("X-Requested-With", "XMLHttpRequest");
            httpClient.DefaultRequestHeaders.Add("Sec-Fetch-Site", "same-origin");
            httpClient.DefaultRequestHeaders.Add("Sec-Fetch-Mode", "cors");
            httpClient.DefaultRequestHeaders.Add("Sec-Fetch-Dest", "empty");
            httpClient.DefaultRequestHeaders.Add("Referer", "https://www.allmusic.com/advanced-search");
            httpClient.DefaultRequestHeaders.Add("Accept-Encoding", "gzip, deflate");
            httpClient.DefaultRequestHeaders.Add("Accept-Language", "en-US,en;q=0.9");

            var response = await httpClient.GetStringAsync(URL);

            var parser = new HtmlDocument();

            parser.LoadHtml(response);

            var names = parser.DocumentNode.SelectNodes("//ul/li/p[1]");

            List<Artist> optionsList = new List<Artist>();
            foreach (var option in names)
            {
                var id = option.Ancestors("li").ToArray()[0].Attributes["data-id"].Value;
                var name = option.InnerText.Trim();
                Artist artistOption = new Artist() { Name = name, Id = id };
                optionsList.Add(artistOption);
            }

            lvResultName.ItemsSource = optionsList;

            
        }

        private void tbSearchArtist_KeyDown_1(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                submitForm();
            }
        }

        private void lvResultName_Selected(object sender, SelectionChangedEventArgs e)
        {
            if (lvResultName.SelectedItems.Count <= 0)
            {
                return;
            }
            var selectedindex = lvResultName.SelectedItem as Artist;
            if (selectedindex != null)
            {
                string artistId = selectedindex.Id;
                string artist = tbSearchArtist.Text;

                SelectAlbums selectAlbums = new SelectAlbums(artistId,artist,this);
                this.Hide();
                selectAlbums.Show();
                lvResultName.SelectedItem = null;

            }
        }
    }
    
}
