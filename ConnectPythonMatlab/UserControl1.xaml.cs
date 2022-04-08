using metabolic_estimation;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
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

namespace ConnectPythonMatlab
{
    /// <summary>
    /// UserControl1.xaml 的交互逻辑
    /// </summary>
    public partial class UserControl1 : UserControl
    {
        string Pyaddress;
        string InterpreterAddress;
        string FileName;
        public string strOutput;

        public UserControl1()
        {
            InitializeComponent();
            GetAddress();

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
            //Matlab = address.ReadLine();
            //MatlabText.Text = Matlab;
        }
        string CallPython(string Pyaddress, string InterpreterAddress, String FileName)
        {
            Process p =OpenCmd();
            p.StandardInput.WriteLine(InterpreterAddress);
            p.StandardInput.WriteLine(@"D:");
            p.StandardInput.WriteLine(@"cd " + Pyaddress);
            p.StandardInput.WriteLine(@"python " + FileName);
            p.StandardInput.WriteLine("exit");
            p.StandardInput.Flush();


            string strOuput = p.StandardOutput.ReadToEnd();


            return strOuput;
            //Console.WriteLine(strOuput);


        }
        public Process OpenCmd()
        {
            Process p = new Process();

            p.StartInfo.FileName = "cmd.exe";
            //p.StartInfo.UseShellExecute = true;
            p.StartInfo.RedirectStandardInput = true;
            p.StartInfo.RedirectStandardOutput = true;
            p.StartInfo.RedirectStandardError = false;
            p.StartInfo.CreateNoWindow = true;

            p.Start();
            return p;
        }

        public void ButtonStart_Click(object sender, RoutedEventArgs e)
        {
            //Class1 DSD = new Class1();
            //DSD.untitled();
            ThreadStart threadStart = new ThreadStart(ThreadCallStart);
            
            Thread thread = new Thread(threadStart);
            thread.Start();






            //OutString.Text = strOutput;
        }
        //绑定委托与事件
        public delegate void CallStartHandler();
        public event CallStartHandler CallStart;



        public void ThreadCallStart()//创建子线程防止卡顿
        {
            strOutput = CallPython(Pyaddress, InterpreterAddress, FileName);
            CallStart();


        }
        public delegate int MyDelegate(string s);
        private void ButtonAddress_Click(object sender, RoutedEventArgs e)
        {
            if (PyAddressText.Text != "")
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

        private void ButtonFileSet_Click(object sender, RoutedEventArgs e)
        {

        }

        private void ButtonFileGet_Click(object sender, RoutedEventArgs e)
        {
            Process p =OpenCmd();
            //string str = this.GetType().Assembly.Location;
            p.StandardInput.WriteLine(@"D:");
            p.StandardInput.WriteLine(@"cd " + Pyaddress);
            p.StandardInput.WriteLine(@"data.xls");
            p.StandardInput.Flush();

        }

        private void TextBox_TextChanged(object sender, TextChangedEventArgs e)
        {

        }

        private void InterpreterAddressText_TextChanged(object sender, TextChangedEventArgs e)
        {

        }

        private void FileNameText_TextChanged(object sender, TextChangedEventArgs e)
        {

        }


        
    }


}
