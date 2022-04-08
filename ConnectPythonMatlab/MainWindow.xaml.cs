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
using System.Threading;

namespace ConnectPythonMatlab
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        //string Pyaddress = @"D:\Doc\SofrWare\matlab_python\ConnectPythonMatlab\file\";
        //string InterpreterAddress = @"conda activate Py3_7";
        //string FileName = @"test315.py";
        //string Matlab = @"metabolic_estimation.xlsx";
        //string Pyaddress ;
        //string InterpreterAddress;
        //string FileName ;
        string strOut;
        UserControl1 control1 = new UserControl1();
        UserControl2 control2 = new UserControl2();

        //string Matlab ;
        public MainWindow()
        {
            InitializeComponent();
            ControlPage.Content = control1;
            //注册事件，以传递strOut
            control2.ButtonStart.Click += control1.ButtonStart_Click;
            // control2.ButtonStart.Click += ButtonStart_Click1;
            //control1.ButtonStart.Click += ButtonStart_Click1;

            control1.CallStart+= CallStartTask;



            // GetAddress();


        }

        private void CallStartTask()
        {
            
            
            strOut = control1.strOutput;
            Dispatcher.Invoke(new Action(() => { control2.OutString.Text = strOut; })); //控件只有主线程可以控制，所以使用Dispatcher.invoke调用主线程，并用action委托执行
            
        }

            
        string CallPython(string Pyaddress,string InterpreterAddress,String FileName)
        {
            Process p = new Process();

            p.StartInfo.FileName = "cmd.exe";
            //p.StartInfo.UseShellExecute = true;
            p.StartInfo.RedirectStandardInput = true;
           p.StartInfo.RedirectStandardOutput = true;
            p.StartInfo.RedirectStandardError = false;
            p.StartInfo.CreateNoWindow = false;

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

             


            //Class1 DSD = new Class1();
            //DSD.untitled();
            //string strOutput = CallPython(Pyaddress, InterpreterAddress,FileName);
            //OutString.Text = strOutput;

            //Thread th = new Thread(new ThreadStart(ThreadMethod));
            //th.Start();

        }
 
        private void GetAddress()
        {
            //StreamReader address = new StreamReader(@"../../../../file/address.txt");
            //Pyaddress = address.ReadLine();
            //PyAddressText.Text = Pyaddress;

            //InterpreterAddress = address.ReadLine();
            //InterpreterAddressText.Text = InterpreterAddress;

            //FileName = address.ReadLine();
            //FileNameText.Text = FileName;

            //Matlab = address.ReadLine();
            //MatlabText.Text = Matlab;
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
            //if(PyAddressText.Text!="")
            //{
            //    Pyaddress = PyAddressText.Text;
            //}
            //if (InterpreterAddressText.Text != "")
            //{
            //    InterpreterAddress = InterpreterAddressText.Text;
            //}
            //if (FileNameText.Text != "")
            //{
            //    FileName = FileNameText.Text;
            //}
            //if (MatlabText.Text != "")
            //{
            //   Matlab = MatlabText.Text;
            //}
        }

        private void FileNameText_Copy_TextChanged(object sender, TextChangedEventArgs e)
        {
            
        }

        public void Page1Click(object sender, RoutedEventArgs e)
        {
            ControlPage.Content = control1;

        }

        private void ButtonStart_Click1(object sender, RoutedEventArgs e)
        {

            strOut = control1.strOutput;

            control2.OutString.Text = strOut;
            // Console.WriteLine("!yes");
        }

        private void Page2Click(object sender, RoutedEventArgs e)
        {
            ControlPage.Content = control2;
        }
    }
}
