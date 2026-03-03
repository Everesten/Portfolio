class Material:
    def __init__(self, id):
        self.id = id
        self.materialType = 'Not Determined'
        self.price = 0
    
    def setPrice(self, price):
        self.price = price

    def getPrice(self):
        return self.price
    
    def setMaterialType(self, materialType):
        self.materialType = materialType
 
    def getMaterialType(self):
        return self.materialType

    def setID(self, id):
        self.id = id
    
    def getID(self):
        return self.id

class ConstructionSite:
    
    def __init__(self, name, city):
            self.name = name
            self.city = city
            self.price = 0
            self.materials = []
    
    def addMaterial(self, material):
        self.materials.append(material)
    
    def findMaterial(self, id):
        for m in self.materials:
            if id == m.getID():
                return m
        return -1

    def calculatePrice(self):
        self.price = 0
        for material in self.materials:
            self.price += material.getPrice()
    
    def countMaterials(self):
        counts = [0, 0, 0]
        for material in self.materials:
            mType = material.getMaterialType()
            if mType == 'WOOD':
                counts[0] += 1
            elif mType == 'STEEL':
                counts[1] += 1
            elif mType == 'BRICK':
                counts[2] += 1
        return counts
    
    def incorporateSite(self, secondary):
        self.materials += secondary.materials
        self.calculatePrice()

    def __str__(self):
        return f'{self.name} site in {self.city} has {len(self.materials)} materials, with a value of {self.price}.'

if __name__ == '__main__':
    
    primary = input()
    secondary = input()

    with open(primary, 'r') as primary:

        name = primary.readline().strip()
        city = primary.readline().strip()

        primSite = ConstructionSite(name, city)

        for i, line in enumerate(primary.readlines()):
            
            line = line.strip()
            id, materialType, price = line.split()
            
            material = Material(id)
            material.setMaterialType(materialType)
            material.setPrice(int(price))
            
            primSite.addMaterial(material)
        
        mCount = primSite.countMaterials()

        primSite.calculatePrice()

        print(f'OUTPUT {primSite}')
        print(f'OUTPUT Wood:{mCount[0]} Steel:{mCount[1]} Brick:{mCount[2]}')

    with open(secondary, 'r') as secondary:
        
        name = secondary.readline().strip()
        city = secondary.readline().strip()

        secSite = ConstructionSite(name, city)

        for i, line in enumerate(secondary.readlines()):
            
            line = line.strip()
            id, materialType, price = line.split()
            
            material = Material(id)
            material.setMaterialType(materialType)
            material.setPrice(int(price))
            
            secSite.addMaterial(material)
        
        mCount = secSite.countMaterials()
        secSite.calculatePrice()

        print(f'OUTPUT {secSite}')
        print(f'OUTPUT Wood:{mCount[0]} Steel:{mCount[1]} Brick:{mCount[2]}')

    primSite.incorporateSite(secSite)
    print(f'OUTPUT {primSite}')