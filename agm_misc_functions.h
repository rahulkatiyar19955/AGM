#pragma once


float str2float(const std::string &s)
{
	if (s.size()<=0)
	{
		printf("dkeiodeji\n");
		WORLDMODELEXCEPTION("dekiehdiwohffhew 3423\n");
	}

	float ret;
	std::string str = s;
	replace(str.begin(), str.end(), ',', '.');
	std::istringstream istr(str);
	istr.imbue(std::locale("C"));
	istr >> ret;
	return ret;
}
