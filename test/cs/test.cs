namespace test
{
    enum state : byte
    {
        ON=1,
        OFF=0
    }

    interface IchargeAble 
    {
        void Charge();
        bool isCharged();
    }

    namespace sub
    {
        public class Inventory{
            public struct weapons{
                public weapons(sword _primary,sword _secondary){
                    primary=_primary;
                    secondary=_secondary;
                }
                public sword primary, secondary;
            }

            weapons weaponSlots;
            public class item
            {
                public virtual void Use()
                {
                
                }
            }

            public class sword : item , IchargeAble
            {
                void Attack()
                {
                
                }

                bool isCharged => true;

                public overide void Use => Attack();
            }
        }
        
    
    }
}