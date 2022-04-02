using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

using metabolic_estimationNative;
using System.Runtime.InteropServices;
using System.IO;

namespace ConnectPythonMatlab
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        string Pyaddress = @"D:\Doc\SofrWare\matlab_python\ConnectPythonMatlab\file\";
        string InterpreterAddress = @"conda activate Py3_7";
        string FileName = @"test315.py";
        public MainWindow()
        {
            InitializeComponent();
            GetAddress();


        }

        string CallPython(string Pyaddress,string InterpreterAddress)
        {
            Process p = new Process();

            p.StartInfo.FileName = "cmd.exe";
            // p.StartInfo.UseShellExecute = true;
            p.StartInfo.RedirectStandardInput = true;
            p.StartInfo.RedirectStandardOutput = true;
            p.StartInfo.RedirectStandardError = false;
            p.StartInfo.CreateNoWindow = true;

            p.Start();
            p.StandardInput.WriteLine(InterpreterAddress);
            p.StandardInput.WriteLine(@"D:");
            p.StandardInput.WriteLine(@"cd "+Pyaddress);
            p.StandardInput.WriteLine(@"python "+FileName);
            p.StandardInput.WriteLine("exit");
            p.StandardInput.Flush();
            string strOuput = p.StandardOutput.ReadToEnd();
            return strOuput;
            //Console.WriteLine(strOuput);
            

        }

        private void ButtonStart_Click(object sender, RoutedEventArgs e)
        {




            Class1 DSD = new Class1();
            DSD.untitled();
            string strOutput = CallPython(Pyaddress, InterpreterAddress);
            OutString.Text = strOutput;
        }
        private void GetAddress()
        {
            StreamReader address = new StreamReader(@"../../../../file/address.txt");
            Pyaddress = address.ReadLine();
            PyAddressText.Text = Pyaddress;
            InterpreterAddress = address.ReadLine();
            InterpreterAddressText.Text = InterpreterAddress;
            FileName = address.ReadLine();
            FileNameText.Text = FileName;
        }
        private void OutString_TextChanged(object sender, TextChangedEventArgs e)
        {
            
        }

        private void OutString_TextInput(object sender, TextCompositionEventArgs e)
        {

        }

        private void TextBox_TextChanged(object sender, TextChangedEventArgs e)
        {

        }

        private void ButtonAddress_Click(object sender, RoutedEventArgs e)
        {
            if(PyAddressText.Text!="")
            {
                Pyaddress = PyAddressText.Text;
            }
            if (InterpreterAddressText.Text != "")
            {
                InterpreterAddress = InterpreterAddressText.Text;
            }
            if (FileNameText.Text != "")
            {
                FileName = FileNameText.Text;
            }
        }
    }
}
