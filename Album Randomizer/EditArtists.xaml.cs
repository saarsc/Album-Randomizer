using System;
using System.Collections.Generic;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace Album_Randomizer
{
    /// <summary>
    /// Interaction logic for EditArtists.xaml
    /// </summary>
    public partial class EditArtists : Window
    {
        public EditArtists()
        {
            InitializeComponent();


            Expander expander = new Expander();
            List<CheckBox> checkBoxes = new List<CheckBox>();

            CheckBox t1 = new CheckBox();
            t1.Content = "test1";

            CheckBox t2 = new CheckBox();
            t2.Content = "test2";

            CheckBox t3 = new CheckBox();
            t3.Content = "test3";

            checkBoxes.Add(t1);
            checkBoxes.Add(t2);
            checkBoxes.Add(t3);

            expander.Content = checkBoxes;

            wrapper.= expander;
        }
    }
}
