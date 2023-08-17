using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace epigeneticagency;

public delegate Map? Action(Map map, Direction direction, ILocationHaver source);