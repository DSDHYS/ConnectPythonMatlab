using System;

namespace Try
{
    class Program
    {
        static void Main()
        {
            int num=4;

            string Str = System.Environment.CurrentDirectory;
            string[] StrSplit =Str.Split("\\");
            string StrAddress = "";
            for (int i = 0; i < num; i++)
            {
               StrAddress += StrSplit[i];
                StrAddress +=@"\\";

            }

            Console.WriteLine(StrAddress);

        }
        private string GetAddressWithNum(int num)
        {
            string Str = System.Environment.CurrentDirectory;
            string[] StrSplit = Str.Split("\\");
            string StrAddress = "";
            for (int i = 0; i < num; i++)
            {
                StrAddress += StrSplit[i];
                StrAddress += @"\\";

            }
            return StrAddress;
        }
    }
}
