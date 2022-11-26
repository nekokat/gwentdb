#include <iostream>
#include <vector>
#include <map>


using namespace std;


map<string, string> TOP_LINE{
    {"left", "\xC9"},
    {"right", "\xBB"},
    {"line", "\xCD"},
    {"sep", "\xCB"}
};

map<string, string> MIDDLE_LINE{
    {"left", "\xCC"},
    {"right", "\xB9"},
    {"line", "\xCD"},
    {"sep", "\xCE"}
};

map<string, string> BOTTOM_LINE{
    {"left", "\xC8"},
    {"right", "\xBC"},
    {"line", "\xCD"},
    {"sep", "\xCA"}
};

string ROW_SEPARATOR = "\xBA";


class Border {
public:
    map<string, string> top_line;
    map<string, string> middle_line;
    map<string, string> bottom_line;
    map<string, string> row_style;
    string _row_separator;
    vector<int> _column_size = {3,2,5,6,7,8,9};
    string DrawLine(map<string, string>);
    Border() {
        top_line = TOP_LINE;
        middle_line = MIDDLE_LINE;
        bottom_line = BOTTOM_LINE;
        _row_separator = ROW_SEPARATOR;
        row_style = {
            {"left",  "\x20" + _row_separator},
            {"right", _row_separator + "\x20"},
            {"sep", "\x20" + _row_separator + "\x20"}
        };
    }
};

string Border::DrawLine(map<string, string> line_style) {
    string line = line_style["left"];
    for (int &column: _column_size){
        for (int i = 0; i < column; i++){
            line.append(line_style["line"]);
        }
        line.append(line_style["sep"]);
    }
    return line;
}

int main() {
    Border line;
    cout << line.DrawLine(line.bottom_line) << endl;
    return 0;
}