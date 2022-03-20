from lxml import etree as et
from tkinter import filedialog
filetypes = [('Archivos XML', '*.xml')];

#Pedimos la ruta del manifest del apk
permission1File = filedialog.askopenfile(filetypes=filetypes, defaultextension=filetypes, title="Abrir AndroidManifest del APK");
rutaManifestAPK = permission1File.name;
permission1File.close();
#Pedimos la ruta del manifest del payload
permission2File = filedialog.askopenfile(filetypes=filetypes, defaultextension=filetypes, title="Abrir AndroidManifest del Payload");
rutaManifestPayload = permission2File.name;
permission2File.close();

permissionsInsertar = [];
featuresInsertar = [];
xmlManifestAPK = et.parse(rutaManifestAPK);

#Obtenemos los permisos del manifest del apk
for perm in xmlManifestAPK.xpath("uses-permission"):
    permissionsInsertar.append(perm);
#Obtenemos las features del manifest del apk
for feature in xmlManifestAPK.xpath("uses-feature"):
    featuresInsertar.append(feature);

#Detectamos qué permisos hay en el manifest del payload que no estén ya en el manifest del apk
for perm in et.parse(rutaManifestPayload).xpath("uses-permission"):
    insertar = True;
    for perm2 in permissionsInsertar:
        if perm.xpath("@android:name", namespaces={"android":"http://schemas.android.com/apk/res/android"})[0] == perm2.xpath("@android:name", namespaces={"android":"http://schemas.android.com/apk/res/android"})[0]:
            insertar = False;
            break;
    if insertar:
        permissionsInsertar.append(perm);
#Detectamos qué features hay en el manifest del payload que no estén ya en el manifest del apk
for feature in et.parse(rutaManifestPayload).xpath("uses-feature"):
    insertar = True;
    for feature2 in featuresInsertar:
        if feature2.xpath("@android:name", namespaces={"android":"http://schemas.android.com/apk/res/android"})[0] == feature2.xpath("@android:name", namespaces={"android":"http://schemas.android.com/apk/res/android"})[0]:
            insertar = False;
            break;
    if insertar:
        featuresInsertar.append(feature);
#Añadimos las features al array de los permisos para escribirlos en el nuevo manifest
for feature in featuresInsertar:
    permissionsInsertar.append(feature);

#Insertamos los nuevos permisos y features que no estén ya establecidos en el manifest, después del primer permiso del manifest del apk
firstPermission = xmlManifestAPK.find("//uses-permission");
parent = firstPermission.getparent();
index = parent.index(firstPermission)+1;
for perm in permissionsInsertar:
    parent.insert(index, perm);
    index+=1;

#Guardamos el nuevo manifest
toSave = filedialog.asksaveasfile(filetypes=filetypes, defaultextension=filetypes, title="Guardar nuevo xml")
pathToSave = toSave.name;
toSave.close();

xmlManifestAPK.write(pathToSave, encoding='utf-8', xml_declaration=True);

