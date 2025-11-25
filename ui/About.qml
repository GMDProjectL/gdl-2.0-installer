import org.kde.kirigamiaddons.formcard as FormCard
import org.kde.coreaddons

FormCard.AboutPage {
    title: translatorBackend.translate("About", translatorBackend.language)
    aboutData: {
        "displayName": "Project GDL",
        "shortDescription": translatorBackend.translate("Project GDL installer written in Python/Kirigami", translatorBackend.language),
        "otherText" : "Optional text shown in the About",
        "version": "1.0",
        "bugAddress": "",
        "homepage" : "https://kde.org",
        "bugAddress" : "",
        "authors" : [
            {
                "name" : "Andrew Relaive",
                "task" : "Main developer"
            }
        ],
        "licenses" : [
            {
                "name" : "The MIT License",
                "text" : `Copyright 2025 Project GDL

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files 
(the “Software”), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, 
publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice 
shall be included in all copies or substantial 
portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT 
WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR 
THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.`,
                "spdx" : "MIT"
            }
        ],
        "copyrightStatement" : "Project GDL, 2023",
    }
}