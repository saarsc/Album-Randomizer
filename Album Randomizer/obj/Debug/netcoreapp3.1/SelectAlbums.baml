   M S B A M L   `   `   `  ����K  GAlbum Randomizer, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null3clr-namespace:Album_RandomizerAlbum_Randomizer  5   	   #    Album_Randomizer.SelectAlbums   5   	   \ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35^ ZWindowsFormsIntegration, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35H 9http://schemas.microsoft.com/winfx/2006/xaml/presentation      5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   0localclr-namespace:Album_Randomizer     5   	     � Title$  SelectAlbums��5   	   $	��450��6   $	��800��6+   .��5	      � .+�5
   
   �� -   5         ��Name$ 	lbWrapper��5
      $��0,0,0,39q�6&    �� View 5      �� 5      ! �� ColumnHeaderContainerStyle 5      �� 5       �� 
TargetType" ��6    .�5      ��  �� Property � �� �� Value 5   "   �� 5   &   .R�5   *   �� -   5        $�� ��5   3    d� 	IsChecked$
 TrueY�6>   6k   5   '   5      5      P�5      �� 5       �� CellTemplate 5      �� 5   "   .R�5   &   �� 
	 � Tag	 6/   �� *ID+ 6B   �� *
selected+��6a   �� *Name+5   #   5       5$      .@�5&      �� $	��100��6   $	��100��6#   5'      �� 5(   
   -   5        
 ��Name$
 
btnConfirm��5(      $��Confirm��6%   $
��Left=�67   $��707,399,0,0q�6R   $	��Top=�6g   $��22��6   $��62��6�    �� 	IsDefault$
 True��6�    J� RenderTransformOrigin$ 
0.129,0.32&�6�   �� 5)   
   -   5        $
 	btnCancel��5)      $��Cancel��6$   $
��Left=�65   $��605,400,0,0q�6P   $	��Top=�6e   $��20��6}   $��54��6�    �� IsCancel$
 True��6�   5+      5,      